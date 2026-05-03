/** @odoo-module **/

import { Component, onMounted, onWillUnmount, useRef, useState, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { loadJS, loadCSS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const LEAFLET_JS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
const LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";

const DEFAULT_LAT = 24.7136;
const DEFAULT_LON = 46.6753;
const DEFAULT_ZOOM = 13;

export class GeofenceMap extends Component {
    static template = "geofence_attendance.GeofenceMap";
    static props = { ...standardFieldProps };

    setup() {
        this.mapContainer = useRef("mapContainer");
        this.searchInput = useRef("searchInput");
        this.state = useState({ loading: true, error: false });

        this._map = null;
        this._marker = null;
        this._circle = null;

        onMounted(async () => {
            try {
                await loadCSS(LEAFLET_CSS);
                await loadJS(LEAFLET_JS);
                this._initMap();
                this.state.loading = false;
            } catch (e) {
                this.state.loading = false;
                this.state.error = true;
            }
        });

        onWillUpdateProps((nextProps) => {
            this._syncFromRecord(nextProps.record);
        });

        onWillUnmount(() => {
            if (this._map) {
                this._map.remove();
                this._map = null;
            }
        });
    }

    get currentLat() {
        return this.props.record.data.geofence_latitude;
    }

    get currentLon() {
        return this.props.record.data.geofence_longitude;
    }

    get currentRadius() {
        return this.props.record.data.geofence_radius || 100;
    }

    _initMap() {
        if (!this.mapContainer.el || !window.L) return;

        const lat = this.currentLat || DEFAULT_LAT;
        const lon = this.currentLon || DEFAULT_LON;
        const hasCoords = !!(this.currentLat || this.currentLon);

        this._map = window.L.map(this.mapContainer.el, {
            center: [lat, lon],
            zoom: hasCoords ? 16 : DEFAULT_ZOOM,
            scrollWheelZoom: true,
        });

        window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors',
        }).addTo(this._map);

        if (hasCoords) {
            this._drawMarkerAndCircle(lat, lon);
        }

        this._map.on("click", (event) => this._onMapClick(event));

        // Force layout refresh in case the form was hidden during init
        setTimeout(() => {
            if (this._map) {
                this._map.invalidateSize();
            }
        }, 200);
    }

    _drawMarkerAndCircle(lat, lon) {
        if (!this._map || !window.L) return;

        if (this._marker) {
            this._marker.setLatLng([lat, lon]);
        } else {
            this._marker = window.L.marker([lat, lon], { draggable: true }).addTo(this._map);
            this._marker.on("dragend", (event) => {
                const pos = event.target.getLatLng();
                this._writeCoordinates(pos.lat, pos.lng);
            });
        }

        if (this._circle) {
            this._circle.setLatLng([lat, lon]);
            this._circle.setRadius(this.currentRadius);
        } else {
            this._circle = window.L.circle([lat, lon], {
                radius: this.currentRadius,
                color: "#2163E8",
                fillColor: "#2163E8",
                fillOpacity: 0.15,
                weight: 2,
            }).addTo(this._map);
        }
    }

    async _onMapClick(event) {
        const { lat, lng } = event.latlng;
        await this._writeCoordinates(lat, lng);
        if (this._map) {
            this._map.panTo([lat, lng]);
        }
    }

    async _writeCoordinates(lat, lon) {
        const roundedLat = Math.round(lat * 1e7) / 1e7;
        const roundedLon = Math.round(lon * 1e7) / 1e7;
        await this.props.record.update({
            geofence_latitude: roundedLat,
            geofence_longitude: roundedLon,
        });
        this._drawMarkerAndCircle(roundedLat, roundedLon);
    }

    _syncFromRecord(record) {
        const lat = record.data.geofence_latitude;
        const lon = record.data.geofence_longitude;
        if (!this._map || !lat || !lon) return;

        this._drawMarkerAndCircle(lat, lon);
    }

    async onSearch(ev) {
        if (ev.key !== "Enter") return;
        ev.preventDefault();
        const query = (this.searchInput.el && this.searchInput.el.value || "").trim();
        if (!query) return;

        try {
            const url = "https://nominatim.openstreetmap.org/search?format=json&limit=1&q="
                + encodeURIComponent(query);
            const response = await fetch(url, { headers: { "Accept": "application/json" } });
            if (!response.ok) return;
            const results = await response.json();
            if (!results || !results.length) return;

            const lat = parseFloat(results[0].lat);
            const lon = parseFloat(results[0].lon);
            if (isNaN(lat) || isNaN(lon)) return;

            await this._writeCoordinates(lat, lon);
            if (this._map) {
                this._map.setView([lat, lon], 17);
            }
        } catch (_e) {
            // Search is best-effort; ignore network errors.
        }
    }

    onUseMyLocation() {
        if (!navigator.geolocation) return;
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                await this._writeCoordinates(lat, lon);
                if (this._map) {
                    this._map.setView([lat, lon], 17);
                }
            },
            () => { /* permission denied or unavailable */ },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }
}

export const geofenceMap = {
    component: GeofenceMap,
    supportedTypes: ["char", "selection"],
    displayName: _t("Geofence Map"),
};

registry.category("fields").add("geofence_map", geofenceMap);

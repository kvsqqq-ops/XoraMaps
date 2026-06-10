from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# =========================
# БАЗОВЫЕ ГОРОДА
# =========================
cities = [
    # Европа
    {"name": "Лондон", "lat": 51.5074, "lon": -0.1278},
    {"name": "Париж", "lat": 48.8566, "lon": 2.3522},
    {"name": "Берлин", "lat": 52.5200, "lon": 13.4050},
    {"name": "Рим", "lat": 41.9028, "lon": 12.4964},
    {"name": "Мадрид", "lat": 40.4168, "lon": -3.7038},
    {"name": "Варшава", "lat": 52.2297, "lon": 21.0122},
    {"name": "Прага", "lat": 50.0755, "lon": 14.4378},
    {"name": "Вена", "lat": 48.2082, "lon": 16.3738},
    {"name": "Будапешт", "lat": 47.4979, "lon": 19.0402},
    {"name": "Стамбул", "lat": 41.0082, "lon": 28.9784},
    {"name": "Киев", "lat": 50.4501, "lon": 30.5234},
    {"name": "Минск", "lat": 53.9006, "lon": 27.5590},
    {"name": "Москва", "lat": 55.7558, "lon": 37.6173},
    {"name": "Санкт-Петербург", "lat": 59.9343, "lon": 30.3351},
    {"name": "Заводське", "lat": 50.3983, "lon": 33.4064},

    # Кавказ
    {"name": "Тбилиси", "lat": 41.7151, "lon": 44.8271},
    {"name": "Ереван", "lat": 40.1792, "lon": 44.4991},
    {"name": "Баку", "lat": 40.4093, "lon": 49.8671},

    # Центральная Азия
    {"name": "Астана", "lat": 51.1694, "lon": 71.4491},
    {"name": "Алматы", "lat": 43.2389, "lon": 76.8897},
    {"name": "Ташкент", "lat": 41.2995, "lon": 69.2401},
    {"name": "Бишкек", "lat": 42.8746, "lon": 74.5698},
    {"name": "Душанбе", "lat": 38.5598, "lon": 68.7870},
    {"name": "Ашхабад", "lat": 37.9601, "lon": 58.3261},

    # Ближний Восток
    {"name": "Анкара", "lat": 39.9334, "lon": 32.8597},
    {"name": "Тегеран", "lat": 35.6892, "lon": 51.3890},
    {"name": "Багдад", "lat": 33.3152, "lon": 44.3661},
    {"name": "Дамаск", "lat": 33.5138, "lon": 36.2765},
    {"name": "Иерусалим", "lat": 31.7683, "lon": 35.2137},
    {"name": "Эр-Рияд", "lat": 24.7136, "lon": 46.6753},
    {"name": "Дубай", "lat": 25.2048, "lon": 55.2708},
    {"name": "Абу-Даби", "lat": 24.4539, "lon": 54.3773},
    {"name": "Доха", "lat": 25.2854, "lon": 51.5310},

    # Южная Азия
    {"name": "Дели", "lat": 28.6139, "lon": 77.2090},
    {"name": "Мумбаи", "lat": 19.0760, "lon": 72.8777},
    {"name": "Бангалор", "lat": 12.9716, "lon": 77.5946},
    {"name": "Калькутта", "lat": 22.5726, "lon": 88.3639},
    {"name": "Ченнаи", "lat": 13.0827, "lon": 80.2707},
    {"name": "Карачи", "lat": 24.8607, "lon": 67.0011},
    {"name": "Лахор", "lat": 31.5204, "lon": 74.3587},
    {"name": "Исламабад", "lat": 33.6844, "lon": 73.0479},
    {"name": "Дакка", "lat": 23.8103, "lon": 90.4125},

    # Восточная Азия
    {"name": "Пекин", "lat": 39.9042, "lon": 116.4074},
    {"name": "Шанхай", "lat": 31.2304, "lon": 121.4737},
    {"name": "Шэньчжэнь", "lat": 22.5431, "lon": 114.0579},
    {"name": "Гуанчжоу", "lat": 23.1291, "lon": 113.2644},
    {"name": "Гонконг", "lat": 22.3193, "lon": 114.1694},
    {"name": "Токио", "lat": 35.6762, "lon": 139.6503},
    {"name": "Осака", "lat": 34.6937, "lon": 135.5023},
    {"name": "Нагоя", "lat": 35.1815, "lon": 136.9066},
    {"name": "Сеул", "lat": 37.5665, "lon": 126.9780},
    {"name": "Пусан", "lat": 35.1796, "lon": 129.0756},
    {"name": "Пхеньян", "lat": 39.0392, "lon": 125.7625},

    # Юго-Восточная Азия
    {"name": "Бангкок", "lat": 13.7563, "lon": 100.5018},
    {"name": "Ханой", "lat": 21.0278, "lon": 105.8342},
    {"name": "Хошимин", "lat": 10.8231, "lon": 106.6297},
    {"name": "Пномпень", "lat": 11.5564, "lon": 104.9282},
    {"name": "Вьентьян", "lat": 17.9757, "lon": 102.6331},
    {"name": "Янгон", "lat": 16.8409, "lon": 96.1735},
    {"name": "Куала-Лумпур", "lat": 3.1390, "lon": 101.6869},
    {"name": "Сингапур", "lat": 1.3521, "lon": 103.8198},
    {"name": "Джакарта", "lat": -6.2088, "lon": 106.8456},
]

# =========================
# ФАЙЛ С КАСТОМНЫМИ МЕТКАМИ
# =========================
MARKERS_FILE = "markers.json"

if not os.path.exists(MARKERS_FILE):
    with open(MARKERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


def load_markers():
    with open(MARKERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_markers(markers):
    with open(MARKERS_FILE, "w", encoding="utf-8") as f:
        json.dump(markers, f, ensure_ascii=False, indent=4)


# =========================
# HTML
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Xora Satellite Map</title>

    <link rel="stylesheet"
          href="https://unpkg.com/leaflet/dist/leaflet.css"/>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <style>

        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: black;
            font-family: Arial;
        }

        #map {
            width: 100%;
            height: 100vh;
        }

        .panel {
            position: absolute;
            top: 10px;
            left: 10px;

            z-index: 9999;

            background: rgba(0,0,0,0.85);
            color: white;

            padding: 12px;
            border-radius: 12px;

            width: 260px;

            backdrop-filter: blur(8px);
        }

        .panel h2 {
            margin-top: 0;
            font-size: 18px;
        }

        .panel input {
            width: 100%;
            margin-bottom: 8px;

            background: #111;
            color: white;

            border: 1px solid #333;
            border-radius: 6px;

            padding: 8px;
            box-sizing: border-box;
        }

        .panel button {
            width: 100%;
            padding: 10px;

            border: none;
            border-radius: 8px;

            background: #00aa66;
            color: white;

            cursor: pointer;
            font-weight: bold;
        }

        .panel button:hover {
            background: #00cc77;
        }

        .coords {
            margin-top: 10px;
            font-size: 13px;
            color: #aaa;
        }

        .leaflet-popup-content {
            font-size: 14px;
        }

    </style>
</head>
<body>

<div class="panel">

    <h2>Xora Map</h2>

    <select id="mapType" onchange="changeMap()" style="width:100%;padding:8px;margin-bottom:8px;background:#111;color:white;border:1px solid #333;border-radius:6px;">
        <option value="satellite">Спутник</option>
        <option value="street">Улицы</option>
        <option value="topo">Топография</option>
        <option value="dark">Тёмная</option>
    </select>

    <input id="markerName" placeholder="Название метки">

    <button onclick="enableAddMode()">
        Поставить метку
    </button>

    <button onclick="clearMarkers()" style="margin-top:8px;background:#aa2222;">
        Удалить ВСЕ кастомные метки
    </button>

    <div class="coords" id="coords">
        LAT: --- <br>
        LON: ---
    </div>

</div>

<div id="map"></div>

<script>

    // =====================
    // КАРТА
    // =====================

    const map = L.map('map').setView([49.0, 32.0], 6);

    const layers = {

        satellite: L.tileLayer(
            'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            {
                attribution: 'Esri World Imagery',
                maxZoom: 18
            }
        ),

        street: L.tileLayer(
            'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                attribution: 'OpenStreetMap',
                maxZoom: 19
            }
        ),

        topo: L.tileLayer(
            'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            {
                attribution: 'OpenTopoMap',
                maxZoom: 17
            }
        ),

        dark: L.tileLayer(
            'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            {
                attribution: 'CartoDB',
                maxZoom: 19
            }
        )
    };

    let currentLayer = layers.satellite;
    currentLayer.addTo(map);

    function changeMap() {

        const type = document.getElementById("mapType").value;

        map.removeLayer(currentLayer);

        currentLayer = layers[type];

        currentLayer.addTo(map);
    }

    // =====================
    // ГОРОДА
    // =====================

    const cities = {{ cities|safe }};
    const customMarkers = {{ custom_markers|safe }};

    const bounds = [];

    cities.forEach(city => {

        bounds.push([city.lat, city.lon]);

        const marker = L.marker([city.lat, city.lon]).addTo(map);

        marker.bindPopup(`
            <b>${city.name}</b><br>
            CITY<br>
            LAT: ${city.lat}<br>
            LON: ${city.lon}
        `);

    });

    // =====================
    // КАСТОМНЫЕ МЕТКИ
    // =====================

    customMarkers.forEach(markerData => {

        const marker = L.circleMarker(
            [markerData.lat, markerData.lon],
            {
                radius: 8,
                color: "red",
                fillColor: "#ff0000",
                fillOpacity: 1
            }
        ).addTo(map);

        marker.bindPopup(`
            <b>${markerData.name}</b><br>
            CUSTOM MARKER<br>
            LAT: ${markerData.lat}<br>
            LON: ${markerData.lon}
        `);

    });

    // =====================
    // FIT
    // =====================

    map.fitBounds(bounds, {
        padding: [50, 50]
    });

    // =====================
    // КООРДЫ КУРСОРА
    // =====================

    map.on('mousemove', function(e) {

        document.getElementById("coords").innerHTML = `
            LAT: ${e.latlng.lat.toFixed(6)}<br>
            LON: ${e.latlng.lng.toFixed(6)}
        `;

    });

    // =====================
    // РЕЖИМ ДОБАВЛЕНИЯ
    // =====================

    let addMode = false;

    function enableAddMode() {

        addMode = true;

        alert("Нажми на карту чтобы поставить метку");

    }

    map.on('click', async function(e) {

        if (!addMode)
            return;

        addMode = false;

        const name =
            document.getElementById("markerName").value || "Unnamed";

        const data = {
            name: name,
            lat: e.latlng.lat,
            lon: e.latlng.lng
        };

        const response = await fetch("/add_marker", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {

            const marker = L.circleMarker(
                [data.lat, data.lon],
                {
                    radius: 8,
                    color: "red",
                    fillColor: "#ff0000",
                    fillOpacity: 1
                }
            ).addTo(map);

            marker.bindPopup(`
                <b>${data.name}</b><br>
                CUSTOM MARKER<br>
                LAT: ${data.lat}<br>
                LON: ${data.lon}
            `);

        }

    });

    // =====================
    // УДАЛЕНИЕ ВСЕХ МЕТОК
    // =====================

    async function clearMarkers() {

        if (!confirm("Удалить все кастомные метки?"))
            return;

        await fetch("/clear_markers", {
            method: "POST"
        });

        location.reload();

    }

    // =====================
    // HOTKEYS
    // =====================

    document.addEventListener("keydown", function(e) {

        // F -> добавить метку
        if (e.key.toLowerCase() === "f") {
            enableAddMode();
        }

        // R -> reload
        if (e.key.toLowerCase() === "r") {
            location.reload();
        }

    });

</script>

</body>
</html>
"""

# =========================
# ROUTES
# =========================

@app.route("/")
def index():

    custom_markers = load_markers()

    return render_template_string(
        HTML,
        cities=json.dumps(cities, ensure_ascii=False),
        custom_markers=json.dumps(custom_markers, ensure_ascii=False)
    )


@app.route("/add_marker", methods=["POST"])
def add_marker():

    data = request.json

    markers = load_markers()

    markers.append({
        "name": data["name"],
        "lat": data["lat"],
        "lon": data["lon"]
    })

    save_markers(markers)

    return jsonify({"success": True})


@app.route("/clear_markers", methods=["POST"])
def clear_markers():

    save_markers([])

    return jsonify({"success": True})


# =========================
# START
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
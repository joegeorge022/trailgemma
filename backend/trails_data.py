"""
Curated Trail & Microclimate Phenology Database
Includes GPS waypoints, canopy composition, elevation profiles, and native flora/fungi markers.
"""

CURATED_TRAILS = [
    {
        "id": "sugarloaf-ridge",
        "name": "Sugarloaf Ridge & Cascade Loop",
        "category": "Autumn Foliage & Trail Run",
        "distance_km": 6.8,
        "elevation_gain_m": 330,
        "avg_elevation_m": 580,
        "difficulty": "Moderate",
        "lat": 44.275,
        "lng": -73.985,
        "canopy_composition": {
            "sugar_maple": 60,
            "red_oak": 25,
            "aspen_birch": 15
        },
        "description": "Spectacular ridge loop known for flaming scarlet sugar maples and a rushing alpine brook.",
        "trailhead": "Cascade Brook Parking Lot, Route 73",
        "chilling_hours_est": 185,
        "waypoints": [
            {"name": "Trailhead & Wooden Footbridge", "lat": 44.275, "lng": -73.985, "elev": 380, "note": "Lush moss, damp leaf carpet."},
            {"name": "Hemlock Ravine & Brook Crossing", "lat": 44.281, "lng": -73.978, "elev": 490, "note": "Listen for Belted Kingfisher and babbling water."},
            {"name": "Scarlet Maple Ridge Overlook", "lat": 44.287, "lng": -73.971, "elev": 690, "note": "Peak canopy panoramic view. 360-degree autumn vibrancy."},
            {"name": "Cascade Falls Crest", "lat": 44.282, "lng": -73.968, "elev": 610, "note": "Crisp granite pools with yellow birch reflections."}
        ],
        "native_flora_markers": [
            {"name": "Sugar Maple (Acer saccharum)", "season": "Peak Anthocyanin Red", "edible": "Spring Sap (Sweet)", "safety": "Safe / Non-toxic"},
            {"name": "Wintergreen (Gaultheria procumbens)", "season": "Bright red berries under leaves", "edible": "Aromatic wintergreen tea leaves", "safety": "Safe in small culinary amounts"},
            {"name": "Chicken of the Woods (Laetiporus sulphureus)", "season": "Vibrant orange shelf fungus", "edible": "Prized edible mushroom on hardwood", "safety": "Caution: must cook thoroughly, avoid if on yew or hemlock"}
        ]
    },
    {
        "id": "pinecrest-valley",
        "name": "Pinecrest River Meadow & Birch Glade",
        "category": "Gentle Nature Walk & Birding",
        "distance_km": 4.2,
        "elevation_gain_m": 95,
        "avg_elevation_m": 240,
        "difficulty": "Easy",
        "lat": 44.182,
        "lng": -73.921,
        "canopy_composition": {
            "sugar_maple": 20,
            "red_oak": 35,
            "aspen_birch": 45
        },
        "description": "Meandering river trail flanked by golden trembling aspens, river birch, and brushy songbird borders.",
        "trailhead": "Meadowbrook Interpretive Shelter",
        "chilling_hours_est": 140,
        "waypoints": [
            {"name": "Riverbend Launch", "lat": 44.182, "lng": -73.921, "elev": 220, "note": "Morning fog lifting off the water."},
            {"name": "Golden Birch Glade", "lat": 44.189, "lng": -73.915, "elev": 245, "note": "Leaves shimmying in the breeze with bright lemon-gold tones."},
            {"name": "Old Mill Pond Marsh", "lat": 44.195, "lng": -73.908, "elev": 255, "note": "Belted Kingfisher perches; Cattail seed fluff dispersing."}
        ],
        "native_flora_markers": [
            {"name": "Paper Birch (Betula papyrifera)", "season": "Peeling white bark & gold leaves", "edible": "Winter survival tea from twigs", "safety": "Safe"},
            {"name": "Staghorn Sumac (Rhus typhina)", "season": "Fuzzy conical red berry clusters", "edible": "Tart wild lemonade infusion", "safety": "Safe (Do not confuse with Poison Sumac which has loose white drooping berries in bogs)"},
            {"name": "Wild Rose Hips (Rosa rugosa / blanda)", "season": "Crimson Vitamin-C rich fruits", "edible": "Rose hip tea / jam (remove inner seeds/hairs)", "safety": "Safe"}
        ]
    },
    {
        "id": "blackwood-crag",
        "name": "Blackwood Crag & Hawk Watch Summit",
        "category": "Summit Hike & Raptor Migration",
        "distance_km": 9.4,
        "elevation_gain_m": 580,
        "avg_elevation_m": 820,
        "difficulty": "Challenging",
        "lat": 44.341,
        "lng": -73.865,
        "canopy_composition": {
            "sugar_maple": 50,
            "red_oak": 30,
            "aspen_birch": 20
        },
        "description": "Steep rocky trail climbing through boreal transition zone to open granite ledges with migrating raptors.",
        "trailhead": "Crag Hollow Trailhead, Gate 4",
        "chilling_hours_est": 245,
        "waypoints": [
            {"name": "Crag Hollow Base", "lat": 44.341, "lng": -73.865, "elev": 460, "note": "Frost pocket in low hollow."},
            {"name": "Switchback Springs", "lat": 44.352, "lng": -73.858, "elev": 680, "note": "Cold natural spring, yellow birch canopy."},
            {"name": "Hawk Watch Ledge", "lat": 44.364, "lng": -73.849, "elev": 920, "note": "Thermal updrafts; watch for Red-tailed Hawks & Sharp-shinned Hawks."},
            {"name": "Blackwood Pinnacle", "lat": 44.369, "lng": -73.842, "elev": 1040, "note": "Stunted balsam fir and panoramic foliage tapestry."}
        ],
        "native_flora_markers": [
            {"name": "Mountain Ash (Sorbus americana)", "season": "Heavy orange-red berry clusters", "edible": "Astringent unless cooked/jellied", "safety": "Mild toxicity raw in large amounts"},
            {"name": "Reindeer Lichen (Cladonia rangiferina)", "season": "Spongy pale green cushions on rock", "edible": "Survival food only (harsh acids)", "safety": "Non-toxic but unpalatable"},
            {"name": "Balsam Fir (Abies balsamea)", "season": "Aromatic needles", "edible": "Vitamin C needle tea", "safety": "Safe (Do not confuse with Yew which is toxic)"}
        ]
    }
]

COMMUNITY_GARDEN_PRESETS = [
    {
        "id": "backyard-raised-beds",
        "name": "Backyard Raised Beds (Slope Microclimate)",
        "elevation_m": 260,
        "dist_water_km": 3.8,
        "slope_aspect_deg": 175, # South facing slope
        "canopy_cover_pct": 20,
        "avg_night_temp_c": 3.2,
        "soil_moisture_pct": 38,
        "day_of_autumn": 38,
        "notes": "Good cold air drainage down the slope; south facing warm soil."
    },
    {
        "id": "valley-bottom-homestead",
        "name": "Valley Floor Homestead (Frost Pocket)",
        "elevation_m": 180,
        "dist_water_km": 0.8,
        "slope_aspect_deg": 40, # North-East slope
        "canopy_cover_pct": 45,
        "avg_night_temp_c": 1.1,
        "soil_moisture_pct": 52,
        "day_of_autumn": 42,
        "notes": "Low hollow collects heavy cold air; high risk of premature frost."
    },
    {
        "id": "urban-rooftop-permaculture",
        "name": "Urban Microclimate Rooftop / Terrace",
        "elevation_m": 120,
        "dist_water_km": 1.2,
        "slope_aspect_deg": 190,
        "canopy_cover_pct": 5,
        "avg_night_temp_c": 6.8,
        "soil_moisture_pct": 30,
        "day_of_autumn": 35,
        "notes": "Thermal mass from masonry stores diurnal heat; extended growing window."
    }
]

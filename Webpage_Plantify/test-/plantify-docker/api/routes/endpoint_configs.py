ENDPOINT_CONFIGS = {
    "all-today": {
        "query": "SELECT * FROM viw_AllValues_Today WHERE pot_id = %s",
        "method": "GET"
    },
    "sunlight-30days": {
        "query": "SELECT * FROM viw_SunlightPerDay_last30Days WHERE pot_id = %s",
        "method": "GET"
    },
    "latest-value": {
        "query": "SELECT * FROM viw_LatestValuePerPot WHERE pot_id = %s",
        "method": "GET"
    },
    "average-mtd": {
        "query": "SELECT * FROM viw_AverageMeasurements_MTD WHERE pot_id = %s",
        "method": "GET"
    },
    "pots": {
        "query": "SELECT * FROM viw_PotsForUser WHERE user_mail = %s",
        "method": "GET"
    },
    "plants": {
        "query": "SELECT * FROM viw_PlantsForUser WHERE user_mail = %s OR user_mail IS NULL",
        "method": "GET"
    },
    "password_hash": {
        "query": "SELECT password_hash FROM user_profile WHERE user_mail = %s",
        "method": "GET"
    },
    "insert-user": {
        "query": "INSERT INTO user_profile(user_mail, password_hash) VALUES(?,?)",
        "params": ["user_mail", "password_hash"],
        "method": "POST"
    },
    "insert-plant": {
        "query": "INSERT INTO plant_profile (name, description, irrigation_cycle_days, target_temperature_celsius, target_sunlight_hours, target_air_humidity_percent, target_soil_moisture_percent) VALUES (?,?,?,?,?,?,?)",
        "params": ["name", "description", "irrigation_cycle_days", "target_temperature_celsius", "target_sunlight_hours", "target_air_humidity_percent", "target_soil_moisture_percent"],
        "method": "POST"
    },
    "insert-user_pot_assignment": {
        "query": "INSERT INTO user_pot_assignment(pot_id, user_id) VALUES(?,?)",
        "params": ["pot_id", "user_id"],
        "method": "POST"
    },
    "insert-plant_pot_assignment": {
        "query": "INSERT INTO plant_pot_assignment(pot_id, plant_id) VALUES(?,?)",
        "params": ["pot_id", "plant_id"],
        "method": "POST"
    },
    "delete-plant_pot_assignment": {
        "query": "UPDATE plant_pot_assignment SET assigned_to = CURRENT_TIMESTAMP WHERE pot_id = ? AND plant_id = ?",
        "params": ["pot_id", "plant_id"],
        "method": "DELETE"
    },
    "delete-user": {
        "query": "DELETE FROM user_profile WHERE user_mail = ?",
        "params": ["user_mail"],
        "method": "DELETE"
    },
    "delete-plant": {
        "query": "DELETE FROM plant_profile WHERE plant_id = ?",
        "params": ["plant_id"],
        "method": "DELETE"
    },
    "delete-pot": {
        "query": "DELETE FROM plant_pot WHERE pot_id = ?",
        "params": ["pot_id"],
        "method": "DELETE"
    },
    "delete-user_pot_assignment": {
        "query": "DELETE FROM user_pot_assignment WHERE pot_id = ? AND user_id = ?",
        "params": ["pot_id", "user_id"],
        "method": "DELETE"
    },
    "update-pot": {
        "query": "UPDATE plant_pot SET pot_name = ? WHERE pot_id = ?",
        "params": ["pot_name","pot_id"],
        "method": "PATCH"
    },
    "update-user_mail": {
        "query": "UPDATE user_profile SET user_mail = ? WHERE user_mail = ?",
        "params": ["user_mail_new","user_mail"],
        "method": "PATCH"
    },
    "update-user_password": {
        "query": "UPDATE user_profile SET password_hash = ? WHERE user_mail = ?",
        "params": ["password_hash","user_mail"],
        "method": "PATCH"
    }
}



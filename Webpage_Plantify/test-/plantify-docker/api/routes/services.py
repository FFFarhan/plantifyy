import mariadb
import sqlite3
from flask import current_app, jsonify, Response
from contextlib import contextmanager
from .endpoint_configs import ENDPOINT_CONFIGS
import os

@contextmanager
def db_cursor():
    # --- ORIGINAL: Try SQLite first, then MariaDB/MySQL ---
    # try:
    #     sqlite_path = '/app/data/plantify.db'
    #     os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    #     connection = sqlite3.connect(sqlite_path)
    #     connection.row_factory = sqlite3.Row
    #     cursor = connection.cursor()
    #     db_type = 'sqlite'
    #     yield connection, cursor, db_type
    # except Exception as sqlite_exc:
    #     # Fallback to MariaDB/MySQL
    #     try:
    #         connection = mariadb.connect(**current_app.config['DB_CONFIG'])
    #         cursor = connection.cursor(dictionary=True)
    #         db_type = 'mariadb'
    #         yield connection, cursor, db_type
    #     except Exception as mariadb_exc:
    #         raise Exception(f"Both SQLite and MariaDB connections failed: {sqlite_exc}, {mariadb_exc}")
    # finally:
    #     try:
    #         cursor.close()
    #         connection.close()
    #     except Exception:
    #         pass

    # --- FORCED: Try MariaDB/MySQL first, then SQLite ---
    try:
        connection = mariadb.connect(**current_app.config['DB_CONFIG'])
        cursor = connection.cursor(dictionary=True)
        db_type = 'mariadb'
        yield connection, cursor, db_type
    except Exception as mariadb_exc:
        # Fallback to SQLite
        try:
            sqlite_path = '/app/data/plantify.db'
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            connection = sqlite3.connect(sqlite_path)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            db_type = 'sqlite'
            yield connection, cursor, db_type
        except Exception as sqlite_exc:
            raise Exception(f"Both MariaDB and SQLite connections failed: {mariadb_exc}, {sqlite_exc}")
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass

def run_query(query, param_values, operation):
    try:
        with db_cursor() as (conn, cursor, db_type):
            # Convert query placeholders and insert ignore for SQLite if needed
            if db_type == 'sqlite':
                query = query.replace('INSERT IGNORE', 'INSERT OR IGNORE')
                query = query.replace('%s', '?')
            cursor.execute(query, tuple(param_values.values()))
            if operation == "fetch":
                rows = cursor.fetchall()
                if db_type == 'sqlite':
                    return jsonify([dict(row) for row in rows])
                return jsonify(rows)
            elif operation == "fetchone":
                row = cursor.fetchone()
                if db_type == 'sqlite':
                    return jsonify(dict(row) if row else None)
                return jsonify(row)
            elif operation in {"insert", "update", "delete"}:
                conn.commit()
                result = {'success': True}
            else:
                return jsonify({'error': f'Unknown operation: {operation}'}), 400
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handle_db_action(endpoint, params, action_type):
    query = ENDPOINT_CONFIGS[endpoint]["query"]

    if action_type == "json":
        allowed_params = {"pot_id", "user_mail"}
        if len(params) != 1 or not set(params.keys()).issubset(allowed_params):
            return Response("Exactly one valid parameter required", status=400)
        param_value = next(iter(params.items()))[1]
        return run_query(query, {"value": param_value}, "fetch")

    elif action_type in {"insert", "update", "delete"}:
        expected_keys = ENDPOINT_CONFIGS[endpoint].get("params", [])
        if not set(expected_keys).issubset(params.keys()):
            return Response("Missing or unexpected parameters", status=400)
        filtered = {k: params[k] for k in expected_keys}
        return run_query(query, filtered, operation=action_type)

    return Response("Unknown action type", status=400)
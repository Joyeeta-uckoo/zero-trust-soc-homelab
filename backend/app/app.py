from flask import Flask, jsonify, render_template
import requests
import json

app = Flask(__name__)

LOKI_URL = "http://loki:3100"


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "SOC Backend"
    })


# =========================================================
# API STATUS
# =========================================================

@app.route("/api")
def api():
    return jsonify({
        "message": "SOC Backend API is running"
    })


# =========================================================
# SECURITY EVENTS
# =========================================================

@app.route("/api/events")
def events():

    # Query Authelia and Traefik logs from Loki
    query = '{container=~"authelia|traefik"}'

    params = {
        "query": query,
        "limit": 100
    }

    try:

        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params=params,
            timeout=10
        )

        response.raise_for_status()

        loki_data = response.json()

        events = []


        # =================================================
        # PROCESS LOKI STREAMS
        # =================================================

        for stream in loki_data.get("data", {}).get("result", []):

            container = stream.get(
                "stream", {}
            ).get(
                "container",
                "unknown"
            )


            # =============================================
            # PROCESS EACH LOG ENTRY
            # =============================================

            for timestamp, log_line in stream.get("values", []):

                event = {
                    "timestamp": timestamp,
                    "source": container,
                    "event": "Log Event",
                    "severity": "info",
                    "category": "System"
                }


                # =========================================
                # AUTHELIA EVENTS
                # =========================================

                if "Unsuccessful 1FA authentication attempt" in log_line:

                    event["event"] = "Failed Authentication"
                    event["severity"] = "high"
                    event["category"] = "Authentication"

                    if "user 'admin'" in log_line:
                        event["user"] = "admin"


                elif "user not found" in log_line.lower():

                    event["event"] = "Unknown User"
                    event["severity"] = "medium"
                    event["category"] = "Authentication"


                elif "authentication succeeded" in log_line.lower():

                    event["event"] = "Successful Authentication"
                    event["severity"] = "info"
                    event["category"] = "Authentication"


                elif "authentication" in log_line.lower():

                    event["event"] = "Authentication Event"
                    event["severity"] = "info"
                    event["category"] = "Authentication"


                # =========================================
                # TRAEFIK EVENTS
                # =========================================

                elif container == "traefik":

                    try:

                        log = json.loads(log_line)

                        status = log.get("DownstreamStatus")

                        event["status"] = status

                        event["method"] = log.get(
                            "RequestMethod"
                        )

                        event["path"] = log.get(
                            "RequestPath"
                        )

                        event["host"] = log.get(
                            "RequestHost"
                        )


                        # ---------------------------------
                        # SUSPICIOUS PATH DETECTION
                        # ---------------------------------

                        path = (
                            event["path"] or ""
                        ).lower()

                        suspicious_paths = [
                            "/.env",
                            "/.git",
                            "/wp-admin",
                            "/wp-login",
                            "/phpmyadmin",
                            "/admin"
                        ]

                        if any(
                            path == suspicious
                            or path.startswith(suspicious + "/")
                            for suspicious in suspicious_paths
                        ):

                            event["event"] = (
                                "Suspicious HTTP Request"
                            )

                            event["severity"] = "high"

                            event["category"] = (
                                "Suspicious Activity"
                            )


                        # ---------------------------------
                        # HTTP 401
                        # ---------------------------------

                        elif status == 401:

                            event["event"] = (
                                "Unauthorized Request"
                            )

                            event["severity"] = "high"

                            event["category"] = "Access"


                        # ---------------------------------
                        # HTTP 403
                        # ---------------------------------

                        elif status == 403:

                            event["event"] = (
                                "Forbidden Request"
                            )

                            event["severity"] = "high"

                            event["category"] = "Access"


                        # ---------------------------------
                        # HTTP 404
                        # ---------------------------------

                        elif status == 404:

                            event["event"] = (
                                "Not Found Request"
                            )

                            event["severity"] = "medium"

                            event["category"] = (
                                "Suspicious Activity"
                            )


                        # ---------------------------------
                        # HTTP 302
                        # ---------------------------------

                        elif status == 302:

                            event["event"] = (
                                "Authentication Redirect"
                            )

                            event["severity"] = "medium"

                            event["category"] = (
                                "Authentication"
                            )


                        # ---------------------------------
                        # HTTP 200
                        # ---------------------------------

                        elif status == 200:

                            event["event"] = (
                                "Successful Request"
                            )

                            event["severity"] = "info"

                            event["category"] = (
                                "Web Traffic"
                            )


                        # ---------------------------------
                        # OTHER HTTP STATUS CODES
                        # ---------------------------------

                        else:

                            event["event"] = "HTTP Request"

                            event["severity"] = "info"

                            event["category"] = (
                                "Web Traffic"
                            )


                    except json.JSONDecodeError:

                        event["event"] = (
                            "Unparsed Traefik Log"
                        )

                        event["severity"] = "info"

                        event["category"] = "System"


                events.append(event)


        # =================================================
        # RETURN STRUCTURED EVENTS
        # =================================================

        return jsonify({
            "count": len(events),
            "events": events
        })


    # =====================================================
    # LOKI CONNECTION ERROR
    # =====================================================

    except requests.RequestException as error:

        return jsonify({
            "error": "Unable to query Loki",
            "details": str(error)
        }), 502


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

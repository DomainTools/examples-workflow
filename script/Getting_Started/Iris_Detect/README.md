# Iris Detect

[User Guide Documentation](https://www.domaintools.com/wp-content/uploads/DomainTools_Iris_Detect_User_Guide.pdf)

[SwaggerHub Documentation](https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DomainTools_APIs/1.1#/)

## `detect_monitors.py`

- An example query using the Iris Detect API to receive the list of monitors created by the org.

## `detect_new_domains.py`

- An example query using the Iris Detect API to receive the list of New domains associated with a specific monitor.
- Make sure to change the monitor_id before running query to receive results for a specific monitor.
- Leaving monitor_id empty will result in the API returning New domains for all monitors.

## `detect_watched_domains.py`

- An example query using the Iris Detect API to receive a list of changed or escalated domains associated with a specific monitor.
- Make sure to change the monitor_id before running query to receive results for a specific monitor.
- See the [SwaggerHub documentation](https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DomainTools_APIs/1.1#/Iris%20Detect/get_v1_iris_detect_domains_watched_) for a better understanding for parameter use cases.

## `detect_ignored_domains.py`

- An example query using the Iris Detect API to receive a list of updates for ignored domains associated with a specific monitor.
- Make sure to change the monitor_id before running query to receive results for a specific monitor.

## `detect_domains_patch.py`

- An example query using the Iris Detect API to add and/or remove domains to/from the watchlist or ignore list.
- Change example domain IDs in order to create successful query
- Analyzing and triaging newly discovered domains is an activity that should be done regularly, so New domains only show recently discovered domains.

## `detect_escalate_domains.py`

- An example query using the Iris Detect API to mark domains to be blocked for internal use or escalate to Google Phishing Protection for review.
- Change example domain IDs in order to create successful query

import dbsettings


class APISettings(dbsettings.Group):
    URLS_UPLOAD_MAX_SIZE = dbsettings.PositiveIntegerValue(default=1024 * 7)
    SEARCH_PAGE_LIMIT = dbsettings.PositiveIntegerValue(default=10)

settings = APISettings('API Settings')
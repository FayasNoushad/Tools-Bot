from .info.cb import info_cb_data
from .qr_code.cb import qr_cb_data
from .translate.cb import tr_cb_data
from .gemini.cb import gemini_cb_data
from .yt_thumb.cb import ytthumb_cb_data
from .country_info.cb import country_cb_data
from .dictionary.cb import dictionary_cb_data


MODULES = {
    "ai": {
        "title": "Gemini AI",
        "command": "ai_help",
        "cb_data": gemini_cb_data,
        "description": "Help message for the AI"
    },
    "info": {
        "title": "Info",
        "command": "info_help",
        "cb_data": info_cb_data,
        "description": "Help message for the info"
    },
    "qr": {
        "title": "QR Code",
        "command": "qr_help",
        "cb_data": qr_cb_data,
        "description": "Help message for the QR"
    },
    "ytthumb": {
        "title": "YouTube Thumbnail",
        "command": "ytthumb_help",
        "cb_data": ytthumb_cb_data,
        "description": "Help message for the YouTube thumbnail"
    },
    "tr": {
        "title": "Translation",
        "command": "tr_help",
        "cb_data": tr_cb_data,
        "description": "Help message for the translation"
    },
    "countryinfo": {
        "title": "Country Information",
        "command": "countryinfo_help",
        "cb_data": country_cb_data,
        "description": "Help message for the country information"
    },
    "dictionary": {
        "title": "Dictionary",
        "command": "dictionary_help",
        "cb_data": dictionary_cb_data,
        "description": "Help message for the dictionary"
    }
}

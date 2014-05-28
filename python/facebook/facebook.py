from __future__ import print_function
import sys
import json

HEADER = {'User-Agent': 'RealTimeWeb Facebook library for educational purposes'}
PYTHON_3 = sys.version_info >= (3, 0)

if PYTHON_3:
    import urllib.error
    import urllib.request as request
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus

################################################################################
# Auxilary
################################################################################


def _parse_float(value, default=0.0):
    """
    Attempt to cast *value* into a float, returning *default* if it fails.
    """
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _iteritems(_dict):
    """
    Internal method to factor-out Py2-to-3 differences in dictionary item
        iterator methods

    :param dict _dict: the dictionary to parse
    :returns: the iterable dictionary
    """
    if PYTHON_3:
        return _dict.items()
    else:
        return _dict.iteritems()


def _urlencode(query, params):
    """
    Internal method to combine the url and params into a single url string.

    :param str query: the base url to query
    :param dict params: the parameters to send to the url
    :returns: a *str* of the full url
    """
    return query + '?' + '&'.join(key+'='+quote_plus(str(value))
                                  for key, value in _iteritems(params))


def _get(url):
    """
    Internal method to convert a URL into it's response (a *str*).

    :param str url: the url to request a response from
    :returns: the *str* response
    """
    if PYTHON_3:
        req = request.Request(url, headers=HEADER)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    else:
        req = urllib2.Request(url, headers=HEADER)
        response = urllib2.urlopen(req)
        return response.read()


def _recursively_convert_unicode_to_str(input):
    """
    Force the given input to only use `str` instead of `bytes` or `unicode`.

    This works even if the input is a dict, list,
    """
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif not PYTHON_3:
        return input.encode('utf-8')
    elif PYTHON_3 and isinstance(input, str):
        return str(input.encode('ascii', 'replace').decode('ascii'))
    else:
        return input


################################################################################
# Cache
################################################################################

_CACHE = {}
_CACHE_COUNTER = {}
_EDITABLE = False
_CONNECTED = True
_PATTERN = "repeat"


def _start_editing(pattern="repeat"):
    """
    Start adding seen entries to the cache. So, every time that you make a request,
    it will be saved to the cache. You must :ref:`_save_cache` to save the
    newly edited cache to disk, though!
    """
    global _EDITABLE, _PATTERN
    _EDITABLE = True
    _PATTERN = pattern


def _stop_editing():
    """
    Stop adding seen entries to the cache.
    """
    global _EDITABLE
    _EDITABLE = False


def _add_to_cache(key, value):
    """
    Internal method to add a new key-value to the local cache.
    :param str key: The new url to add to the cache
    :param str value: The HTTP response for this key.
    :returns: void
    """
    if key in _CACHE:
        _CACHE[key].append(value)
    else:
        _CACHE[key] = [_PATTERN, value]
        _CACHE_COUNTER[key] = 0


def _clear_key(key):
    """
    Internal method to remove a key from the local cache.
    :param str key: The url to remove from the cache
    """
    if key in _CACHE:
        del _CACHE[key]


def _save_cache(filename="cache.json"):
    """
    Internal method to save the cache in memory to a file, so that it can be used later.

    :param str filename: the location to store this at.
    """
    with open(filename, 'w') as f:
        json.dump({"data": _CACHE, "metadata": ""}, f)


def _lookup(key):
    """
    Internal method that looks up a key in the local cache.

    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if key not in _CACHE:
        return ""
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 1
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][_CACHE_COUNTER[key]]
    else:
        return ""


def connect():
    """
    Connect to the online data source in order to get up-to-date information.

    :returns: void
    """
    global _CONNECTED
    _CONNECTED = True


def disconnect(filename="./cache.json"):
    """
    Connect to the local cache, so no internet connection is required.

    :returns: void
    """
    global _CONNECTED, _CACHE
    try:
        with open(filename, 'r') as f:
            _CACHE = _recursively_convert_unicode_to_str(json.load(f))['data']
    except (OSError, IOError) as e:
        raise FacebookException("The cache file '{}' was not found.".format(filename))
    for key in _CACHE.keys():
        _CACHE_COUNTER[key] = 0
    _CONNECTED = False

################################################################################
# Exceptions
################################################################################


class FacebookException(Exception):
    pass


################################################################################
# Domain Objects
################################################################################

class Photo(object):

    """
    A Facebook photo
    """
    def __init__(self, id=None, created_time=None, uploader=None, height=None,
                 width=None, source=None):
        """
        Creates a new photo object.

        :param int id: the Facebook id of the photo
        :param str created_time: the time and date the photo was uploaded
        :param uploader: the uploader of the photo
        #TODO: set uploader type
        :param int height: the height of the photo
        :param int width: the width of the photo
        :param str source: the url of the source image
        """

        self.id = id
        self.created_time = created_time
        self.uploader = uploader
        self.height = height
        self.width = width
        self.source = source

    @staticmethod
    def _from_json(json_data):
        """
        Creates a Photo from JSON data.

        :param json_data: JSON to parse, in this case a photo from an album[]
        :returns: Photo
        """

        if json_data is None:
            return Photo()
        try:
            photo_id = json_data['id']
            created_time = json_data['created_time']
            uploader = json_data['from']  # TODO: wrap?
            height = json_data['images'][0]['height']
            width = json_data['images'][0]['width']
            source = json_data['images'][0]['source']

            photo = Photo(id=photo_id, created_time=created_time, uploader=uploader,
                          height=height, width=width, source=source)
            return photo

        except KeyError:
            raise FacebookException("The given information was incomplete.")


class Message:
    pass


class Like(object):
    """
    A Facebook page the user has liked.
    """
    def __init__(self, category=None, name=None):
        """
        Creates a new Like object.

        :param str category: The top-level category of the page
        :param str name: The name of the Facebook page
        """

        self.category = category
        self.name = name

    @staticmethod
    def _from_json(json_data):
        """
        Creates a Like from JSON data

        :param str json_data: the JSON to parse, in this case a like
        :returns: a Like object
        """

        if json_data is None:
            return Like()
        try:
            category = json_data['category']  # Not really sure what PyCharm
            # has a problem with...
            name = json_data['name']
            like = Like(category=category, name=name)
            return like
        except KeyError:
            raise FacebookException("The given information was incomplete.")


class Status(object):
    """
    A Facebook user's post
    """
    def __init__(self, message=None, tags=None, likes=None):
        """
        Creates a new Status object

        :param str message: The actual text of the status
        :param tags: list of users tagged in the status. Currently broken
        :param likes: list of users who have liked the status
        """

        self.message = message
        self.tags = tags
        self.likes = likes

    @staticmethod
    def _from_json(json_data):
        """
        Creates a new Status object from JSON data

        :param str json_data: The raw JSON to parse, in this case a status dump
        :returns: a new Status object
        """

        message = json_data['message']
        likes = json_data['likes']
        status = Status(message=message, likes=likes)
        return status


class FacebookUser(object):

    """
    A Facebook user
    """
    def __init__(self, albums=None, feed=None, likes=None,
                 name=None, notifications=None, photos=None, statuses=None):

        """
        Creates a new FacebookUser

        :param albums: A list of albums where each album is a dictionary.
        :type albums: list

        :param feed: A list of feed where each feed is a dictionary.
        :type feed: list

        :param likes: A list of likes where each like is a dictionary.
        :type likes: list

        :param name: Your name.
        :type name: str

        :param notifications: A list of notifications where each notification is a dictionary.
        :type notifications: list

        :param photos: A list of photos where each photo is a dictionary.
        :type photos: list

        :param statuses: A list of statuses where each status is a dictionary.
        :type statuses: list
        """

        self.albums = albums
        self.feed = feed
        self.likes = likes
        self.name = name
        self.notifications = notifications
        self.photos = photos
        self.statuses = statuses

    def __unicode__(self):
        return "<FacebookUser Name: {}>".format(self.name)

    def __repr__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def __str__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def _to_dict(self):
        return {'albums': self.albums, 'feed': self.feed,  'likes': self.likes,
                'name': self.name, 'notifications': self.notifications,
                'photos': self.photos, 'statuses': self.statuses}

    @staticmethod
    def _from_json(json_data):
        """
        Creates a FacebookUser from json data.

        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: FacebookUser
        """

        if json_data is None:
            return FacebookUser()
        try:
            json_dict = json_data[0]
            # albums = json_dict['albums']['data']
            # feed = json_dict['feed']['data']
            likes = json_dict['likes']['data']
            list_of_likes = [Like(name=like['name'], category=like['category']) for like in likes]
            # name = json_dict['name']
            # notifications = json_dict['notifications']['data']
            # photos = json_dict['photos']['data']
            statuses = json_dict['statuses']['data']

            user = FacebookUser(likes=likes,
                                statuses=statuses)
            return user
        except KeyError:
            raise FacebookException("The given information was incomplete.")


################################################################################
# Service Methods
################################################################################


def _fetch_facebook_info(params):
    """
    Internal method to form and query the server

    :param dict params: the parameters to pass to the server
    :returns: the JSON response object
    """
    baseurl = 'https://graph.facebook.com/me'
    query = _urlencode(baseurl, params)

    if PYTHON_3:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib.error.HTTPError:
            raise FacebookException("Make sure your token is correct and valid")
    else:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib2.HTTPError:
            raise FacebookException("Make sure your token is correct and valid")

    if not result:
        raise FacebookException("There were no results")

    try:
        if _CONNECTED and _EDITABLE:
            _add_to_cache(query, result)
        json_res = json.loads('[' + result + ']')  # Facebook does not return a
                                                    # list, but returns a string
    except ValueError:
        raise FacebookException("Internal Error")

    return json_res


def get_facebook_information(access_token=None):
    """
    """
    if access_token is None:
        disconnect()

    fields = 'albums,likes'

    params = {'fields': fields, 'access_token': access_token}

    json_res = _fetch_facebook_info(params)
    user = FacebookUser._from_json(json_res)

    return user._to_dict()


def get_messages(access_token=None):
    if access_token is None:
        disconnect()

    return


def _get_photos(album):
    """
    Given a single album, returns a list of Photo objects

    :param dict album: the album to get the photos from
    :returns: list of Photos
    """
    photolist = []
    for photo in album['photos']['data']:
        photolist.append(Photo._from_json(photo))
    return photolist


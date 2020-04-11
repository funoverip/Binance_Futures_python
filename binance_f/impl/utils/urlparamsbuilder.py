import json
import urllib.parse


class UrlParamsBuilder(object):

    def __init__(self):
        self.param_map = dict()
        self.post_map = dict()

    def put_url(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.param_map[name] = json.dumps(value)
            elif isinstance(value, float):
                self.param_map[name] = ('%.20f' % (value))[slice(0, 16)].rstrip('0').rstrip('.')
            else:
                self.param_map[name] = str(value)
    def put_post(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.post_map[name] = value
            else:
                self.post_map[name] = str(value)

    def build_url(self):
        if len(self.param_map) == 0:
            return ""
        # Error -1022: Signature for this request is not valid.
        # => Ensure 'signature' parameter is at the end of the URL, as per doc.
        signature = ''
        if 'signature' in self.param_map:
            # Remove it from the (unsorted) dic and append manually
            signature = self.param_map['signature']
            del self.param_map['signature']
            signature = "&signature=%s" % signature
        encoded_param = urllib.parse.urlencode(self.param_map)
        # Append the signature manually. URL encoding is not necessary here.
        encoded_param += signature
        return encoded_param

    def build_url_to_json(self):
        return json.dumps(self.param_map)

import redis
import event_lib.utils as ut
from event_lib import config


class RedisPython(object):
	def __init__(self, redis_config):
		self.re_client = redis.Redis(**redis_config)

	def set_many(self, data_dict, expiry_time):
		rv = True
		for key, value in data_dict.items():
			value = ut.to_json(value)
			if not self.re_client.set(key, value, expiry_time):
				rv = False
		return rv

	def get_many(self, keys):
		data = self.re_client.mget(keys)
		result = {}
		for key, value in zip(keys, data):
			if value is None:
				continue
			result[key] = ut.from_json(value)
		return result

	def get(self, key):
		ans = self.re_client.get(key)
		return None if ans is None else ut.from_json(ans)

	def set(self, key, val, expiry_time):
		return self.re_client.set(key, ut.to_json(val), expiry_time)

	def remove(self, key):
		return self.re_client.delete(key)


cache = RedisPython(config.CACHE_SERVERS["redis"])

USER_LOGIN_CACHE_SESSION = "%s.user_login_cache_session"

CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID = {
	'cache_prefix': '%s.get_event_detail.by_id',
	'expiry_time': 5 * 60,
	'cache_key_converter': lambda prefix, event_id, *args: prefix % event_id
}

CACHE_KEY_FUNC_GET_EVENT_INFOS_BY_IDS = {
	'cache_prefix': '%s.get_event_infos.by_ids',
	'expiry_time': 5 * 60,
}


CACHE_KEY_FUNC_GET_USER_INFOS_BY_IDS = {
	'cache_prefix': '%s.get_user_infos.by_ids',
	'expiry_time': 5 * 60,
}


def remove_key_cache(key):
	return cache.remove(key)


def set_token_by_user_id(user_id, token, expiry_time):
	return cache.set(USER_LOGIN_CACHE_SESSION % user_id, token, expiry_time)


def get_token_by_user_id(user_id):
	return cache.get(USER_LOGIN_CACHE_SESSION % user_id)


def one_key_cache_data(cache_key_converter, cache_prefix, expiry_time=60):
	def _cache_data(func):
		def _func(*args, **kwargs):
			cache_key = cache_key_converter(cache_prefix, *args)
			data = cache.get(cache_key)
			force_query = kwargs.get("force_query", False)
			if force_query or data is None:
				data = func(*args)
				cache.set(cache_key, data, expiry_time)
			return data
		return _func
	return _cache_data


def cache_data_by_keys(cache_prefix, expiry_time=60):
	def _cache_data_func(func):
		def _func(keys, **kwargs):
			if not keys:
				return {}
			keys = list(set(keys))
			force_query = kwargs.get("force_query", False)
			result_data = {}
			if not force_query:
				cache_key_map = {cache_prefix % key: key for key in keys}
				cached_data_dict = cache.get_many(cache_key_map.keys())
				remove_keys = set()
				for cached_key, cached_data in cached_data_dict.items():
					key = cache_key_map[cached_key]
					result_data[key] = cached_data
					remove_keys.add(key)
				keys = [key for key in keys if key not in remove_keys]
				# log.info("key_cache_hit|cached_key=%s", ','.join(cached_data_dict.keys()))
			if keys:
				response_data = func(keys)
				if response_data:
					data_to_cache = {cache_prefix % key: data for key, data in response_data.items() if data}
					cache.set_many(data_to_cache, expiry_time)
				return {**result_data, **response_data}
			else:
				return result_data

		return _func

	return _cache_data_func

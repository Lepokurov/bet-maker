import httpx

from settings import (
    LINE_PROVIDER_API_HOST_URL,
    LINE_PROVIDER_API_TOKEN,
    SERVICE_NAME,
)


class LineProviderClient:
    __get_events_url = f"{LINE_PROVIDER_API_HOST_URL}/api/events"
    __get_event_url = f"{LINE_PROVIDER_API_HOST_URL}/api/events/{{event_id}}"

    async def __aenter__(self, *args, **kwargs) -> "LineProviderClient":
        headers = {"User-Agent": SERVICE_NAME, "Authorization": f"Bearer {LINE_PROVIDER_API_TOKEN}"}
        self._client = httpx.AsyncClient(headers=headers, follow_redirects=True)
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self._client.aclose()

    async def get_events(self):
        resp = await self._client.get(self.__get_events_url, params={"is_actual": True})
        if resp.status_code != 200:
            return {}
        data = resp.json()
        return data

    async def get_event(self, event_id):
        resp = await self._client.get(self.__get_event_url.format(event_id=event_id))
        if resp.status_code != 200:
            return {}
        data = resp.json()
        return data


async def get_line_provider_client() -> LineProviderClient:
    async with LineProviderClient() as session:
        yield session

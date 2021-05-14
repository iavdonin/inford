from .service_base import ServiceBase


class GetRecommendations(ServiceBase):
    def __init__(self, portfolio):
        self.portfolio = portfolio

    async def execute(self):
        return recommend(self.portfolio)


def recommend(portfolio):
    return {'recommendations': [{'Sberbank': 100}, {'Sberbank again': 200}]}

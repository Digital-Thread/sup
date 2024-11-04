from dishka import Provider, Scope, provide

from src.apps.feature import (
    CreateFeatureInteractor,
    DeleteFeatureInteractor,
    GetAllFeaturesInteractor,
    GetFeatureInteractor,
    UpdateFeatureInteractor,
)


class FeatureInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_feature = provide(CreateFeatureInteractor)
    get_feature_by_id = provide(GetFeatureInteractor)
    get_features = provide(GetAllFeaturesInteractor)
    update_feature = provide(UpdateFeatureInteractor)
    delete_feature = provide(DeleteFeatureInteractor)

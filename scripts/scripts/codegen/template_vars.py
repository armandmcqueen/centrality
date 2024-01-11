from dataclasses import dataclass
import inspect


@dataclass
class TemplateVars:
    metric_obj_fields: str
    metric_name_lowercase: str
    metric_name_camelcase: str
    metric_name_capitalized: str
    metrics_shape_db: str
    metrics_type_db: str
    example_metrics: str
    custom_types: str
    convert_from_metrics_fn_str: str
    convert_to_metrics_fn_str: str

    @classmethod
    def from_module(cls, module):
        return cls(
            metric_obj_fields=module.metric_obj_fields,
            metric_name_lowercase=module.metric_name_lowercase,
            metric_name_camelcase=module.metric_name_camelcase,
            metric_name_capitalized=module.metric_name_capitalized,
            metrics_shape_db=module.metrics_shape_db,
            metrics_type_db=module.metrics_type_db,
            example_metrics=module.example_metrics,
            custom_types=module.custom_types,
            convert_from_metrics_fn_str=inspect.getsource(module.convert_from_metrics),
            convert_to_metrics_fn_str=inspect.getsource(module.convert_to_metrics),
        )

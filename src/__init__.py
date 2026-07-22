"""
src — Ethiopia Financial Inclusion project package
===================================================
Public API re-exports so callers can import directly from `src`:

    from src import load_unified_data, load_reference_codes
    from src import validate_record, print_schema_summary
    from src import plot_account_ownership_trajectory, plot_event_timeline
"""

from .data_loader import (
    load_unified_data,
    load_reference_codes,
    get_observations,
    get_events,
    get_impact_links,
    get_targets,
    get_by_pillar,
    join_events_to_impact_links,
)

from .schema_utils import (
    validate_record,
    validate_dataframe,
    print_schema_summary,
    make_observation,
    make_event,
    make_impact_link,
    RECORD_TYPES,
    PILLARS,
    CONFIDENCE_LEVELS,
    SOURCE_TYPES,
)

from .visualization import (
    plot_record_type_distribution,
    plot_pillar_distribution,
    plot_confidence_distribution,
    plot_source_type_distribution,
    plot_temporal_coverage,
    plot_account_ownership_trajectory,
    plot_gender_gap,
    plot_mobile_money_penetration,
    plot_event_timeline,
)

__all__ = [
    # data_loader
    "load_unified_data",
    "load_reference_codes",
    "get_observations",
    "get_events",
    "get_impact_links",
    "get_targets",
    "get_by_pillar",
    "join_events_to_impact_links",
    # schema_utils
    "validate_record",
    "validate_dataframe",
    "print_schema_summary",
    "make_observation",
    "make_event",
    "make_impact_link",
    "RECORD_TYPES",
    "PILLARS",
    "CONFIDENCE_LEVELS",
    "SOURCE_TYPES",
    # visualization
    "plot_record_type_distribution",
    "plot_pillar_distribution",
    "plot_confidence_distribution",
    "plot_source_type_distribution",
    "plot_temporal_coverage",
    "plot_account_ownership_trajectory",
    "plot_gender_gap",
    "plot_mobile_money_penetration",
    "plot_event_timeline",
]

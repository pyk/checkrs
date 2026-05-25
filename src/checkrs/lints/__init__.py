"""Registered checkrs lints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.allow_dead_code import AllowDeadCode
from checkrs.lints.allow_unused_imports import AllowUnusedImports
from checkrs.lints.anonymous_tuple_returns import AnonymousTupleReturns
from checkrs.lints.anyhow_bail_prefix import AnyhowBailPrefix
from checkrs.lints.anyhow_context_format import AnyhowContextFormat
from checkrs.lints.anyhow_ensure_usage import AnyhowEnsureUsage
from checkrs.lints.anyhow_is_empty_bail import AnyhowIsEmptyBail
from checkrs.lints.anyhow_is_some_bail import AnyhowIsSomeBail
from checkrs.lints.anyhow_map_err import AnyhowMapErr
from checkrs.lints.anyhow_match_option_context import AnyhowMatchOptionContext
from checkrs.lints.anyhow_ok_or_else import AnyhowOkOrElse
from checkrs.lints.anyhow_prefer_context import AnyhowPreferContext
from checkrs.lints.anyhow_result_prefix import AnyhowResultPrefix
from checkrs.lints.as_limbs_truncation import AsLimbsTruncation
from checkrs.lints.block_doc_comments import BlockDocComments
from checkrs.lints.box_leak_usage import BoxLeakUsage
from checkrs.lints.cfg_test_use import CfgTestUse
from checkrs.lints.clap_subcommand_prefix import ClapSubcommandPrefix
from checkrs.lints.clone_in_iterator import CloneInIterator
from checkrs.lints.clone_in_loops import CloneInLoops
from checkrs.lints.continue_in_err_arm import ContinueInErrArm
from checkrs.lints.crate_import_order import CrateImportOrder
from checkrs.lints.em_dash_in_comments import EmDashInComments
from checkrs.lints.error_handling_in_filter_map import ErrorHandlingInFilterMap
from checkrs.lints.expect_usage import ExpectUsage
from checkrs.lints.extra_space_after_period import ExtraSpaceAfterPeriod
from checkrs.lints.ignore_in_doc_tests import IgnoreInDocTests
from checkrs.lints.ignored_writeln_result import IgnoredWritelnResult
from checkrs.lints.immediately_invoked_closures import ImmediatelyInvokedClosures
from checkrs.lints.inconsistent_example_headers import InconsistentExampleHeaders
from checkrs.lints.intermediate_clones import IntermediateClones
from checkrs.lints.is_some_and_deep_match import IsSomeAndDeepMatch
from checkrs.lints.long_if_let_blocks import LongIfLetBlocks
from checkrs.lints.match_panic_to_let_else import MatchPanicToLetElse
from checkrs.lints.missing_file_module_docs import MissingFileModuleDocs
from checkrs.lints.mod_rs_missing_docs import ModRsMissingDocs
from checkrs.lints.must_use_attribute import MustUseAttribute
from checkrs.lints.negated_contains_in_conditions import NegatedContainsInConditions
from checkrs.lints.nested_if_let import NestedIfLet
from checkrs.lints.non_test_module_declarations import NonTestModuleDeclarations
from checkrs.lints.owned_string_parameters import OwnedStringParameters
from checkrs.lints.panic_usage import PanicUsage
from checkrs.lints.path_field_types import PathFieldTypes
from checkrs.lints.path_param_types import PathParamTypes
from checkrs.lints.prefer_filter_map import PreferFilterMap
from checkrs.lints.pretty_assertions_prefix import PrettyAssertionsPrefix
from checkrs.lints.revm_bytecode_bytecode_prefix import RevmBytecodeBytecodePrefix
from checkrs.lints.revm_database_cachedb_prefix import RevmDatabaseCachedbPrefix
from checkrs.lints.revm_database_inmemorydb_prefix import RevmDatabaseInmemorydbPrefix
from checkrs.lints.revm_primitives_bytes_prefix import RevmPrimitivesBytesPrefix
from checkrs.lints.scraper_element_ref_prefix import ScraperElementRefPrefix
from checkrs.lints.self_imports import SelfImports
from checkrs.lints.serde_clone_into_from_value import SerdeCloneIntoFromValue
from checkrs.lints.serde_enum_tag import SerdeEnumTag
from checkrs.lints.std_exitcode_prefix import StdExitcodePrefix
from checkrs.lints.std_fs_prefix import StdFsPrefix
from checkrs.lints.std_hashmap_prefix import StdHashmapPrefix
from checkrs.lints.std_hashset_prefix import StdHashsetPrefix
from checkrs.lints.std_import_order import StdImportOrder
from checkrs.lints.std_path_prefix import StdPathPrefix
from checkrs.lints.std_process_prefix import StdProcessPrefix
from checkrs.lints.std_sync_arc_prefix import StdSyncArcPrefix
from checkrs.lints.super_imports import SuperImports
from checkrs.lints.test_prefix_in_names import TestPrefixInNames
from checkrs.lints.to_string_instead_of_into import ToStringInsteadOfInto
from checkrs.lints.tracing_info_prefix import TracingInfoPrefix
from checkrs.lints.turbofish_collect import TurbofishCollect
from checkrs.lints.underscore_in_types import UnderscoreInTypes
from checkrs.lints.unnecessary_doc_sections import UnnecessaryDocSections
from checkrs.lints.unsafe_usage import UnsafeUsage
from checkrs.lints.unwrap_usage import UnwrapUsage
from checkrs.lints.use_after_mod import UseAfterMod
from checkrs.lints.use_inside_blocks import UseInsideBlocks

if TYPE_CHECKING:
    from checkrs.lints.lint import Lint


def get_all_lints() -> list[Lint]:
    """Return all registered lints."""
    return [
        ModRsMissingDocs(),
        AsLimbsTruncation(),
        AnyhowBailPrefix(),
        AnyhowContextFormat(),
        AnyhowIsEmptyBail(),
        AnyhowIsSomeBail(),
        AnyhowMapErr(),
        AnyhowOkOrElse(),
        AnyhowPreferContext(),
        AnyhowMatchOptionContext(),
        AnyhowEnsureUsage(),
        AnyhowResultPrefix(),
        RevmDatabaseInmemorydbPrefix(),
        RevmDatabaseCachedbPrefix(),
        RevmBytecodeBytecodePrefix(),
        RevmPrimitivesBytesPrefix(),
        PrettyAssertionsPrefix(),
        MissingFileModuleDocs(),
        AllowDeadCode(),
        AllowUnusedImports(),
        AnonymousTupleReturns(),
        CloneInIterator(),
        CloneInLoops(),
        ErrorHandlingInFilterMap(),
        ExpectUsage(),
        ExtraSpaceAfterPeriod(),
        LongIfLetBlocks(),
        IgnoreInDocTests(),
        ImmediatelyInvokedClosures(),
        InconsistentExampleHeaders(),
        IntermediateClones(),
        IsSomeAndDeepMatch(),
        MustUseAttribute(),
        NegatedContainsInConditions(),
        NestedIfLet(),
        NonTestModuleDeclarations(),
        PanicUsage(),
        SelfImports(),
        StdHashmapPrefix(),
        StdHashsetPrefix(),
        StdFsPrefix(),
        StdPathPrefix(),
        StdExitcodePrefix(),
        StdProcessPrefix(),
        StdSyncArcPrefix(),
        OwnedStringParameters(),
        SuperImports(),
        TestPrefixInNames(),
        TurbofishCollect(),
        UnderscoreInTypes(),
        UnsafeUsage(),
        UnwrapUsage(),
        UseAfterMod(),
        UseInsideBlocks(),
        BlockDocComments(),
        BoxLeakUsage(),
        CfgTestUse(),
        ClapSubcommandPrefix(),
        CrateImportOrder(),
        EmDashInComments(),
        PathFieldTypes(),
        PathParamTypes(),
        PreferFilterMap(),
        ContinueInErrArm(),
        MatchPanicToLetElse(),
        UnnecessaryDocSections(),
        IgnoredWritelnResult(),
        ToStringInsteadOfInto(),
        StdImportOrder(),
        ScraperElementRefPrefix(),
        SerdeEnumTag(),
        SerdeCloneIntoFromValue(),
        TracingInfoPrefix(),
    ]

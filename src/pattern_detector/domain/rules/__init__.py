"""Rule catalog registration for Go pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.abstract_factory_rule import AbstractFactoryRule
from pattern_detector.domain.rules.adapter_rule import AdapterPatternRule
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.bridge_rule import BridgePatternRule
from pattern_detector.domain.rules.builder_rule import BuilderPatternRule
from pattern_detector.domain.rules.chain_of_responsibility_rule import ChainOfResponsibilityRule
from pattern_detector.domain.rules.circular_dependency_rule import CircularDependencyRule
from pattern_detector.domain.rules.cohesion_coupling_rule import HighCohesionLowCouplingRule
from pattern_detector.domain.rules.command_rule import CommandPatternRule
from pattern_detector.domain.rules.composite_rule import CompositePatternRule
from pattern_detector.domain.rules.context_propagation_rule import ContextPropagationRule
from pattern_detector.domain.rules.decorator_rule import DecoratorPatternRule
from pattern_detector.domain.rules.dip_rule import DependencyInversionRule
from pattern_detector.domain.rules.dry_rule import DryRule
from pattern_detector.domain.rules.errgroup_concurrency_rule import ErrgroupConcurrencyRule
from pattern_detector.domain.rules.facade_rule import FacadePatternRule
from pattern_detector.domain.rules.factory_rule import FactoryMethodRule
from pattern_detector.domain.rules.fan_out_fan_in_rule import FanOutFanInRule
from pattern_detector.domain.rules.flyweight_rule import FlyweightPatternRule
from pattern_detector.domain.rules.functional_options_rule import FunctionalOptionsRule
from pattern_detector.domain.rules.generator_rule import GeneratorPatternRule
from pattern_detector.domain.rules.goroutine_leak_rule import GoroutineLeakRule
from pattern_detector.domain.rules.interface_pollution_rule import InterfacePollutionRule
from pattern_detector.domain.rules.interpreter_rule import InterpreterPatternRule
from pattern_detector.domain.rules.iterator_rule import IteratorPatternRule
from pattern_detector.domain.rules.kiss_rule import KissRule
from pattern_detector.domain.rules.law_of_demeter_rule import LawOfDemeterRule
from pattern_detector.domain.rules.lsp_rule import LiskovSubstitutionRule
from pattern_detector.domain.rules.mediator_rule import MediatorPatternRule
from pattern_detector.domain.rules.memento_rule import MementoPatternRule
from pattern_detector.domain.rules.observer_rule import ObserverPatternRule
from pattern_detector.domain.rules.ocp_rule import OpenClosedPrincipleRule
from pattern_detector.domain.rules.pipeline_rule import PipelinePatternRule
from pattern_detector.domain.rules.prototype_rule import PrototypePatternRule
from pattern_detector.domain.rules.proxy_rule import ProxyPatternRule
from pattern_detector.domain.rules.singleton_rule import SingletonPatternRule
from pattern_detector.domain.rules.srp_rule import SingleResponsibilityRule
from pattern_detector.domain.rules.state_rule import StatePatternRule
from pattern_detector.domain.rules.strategy_rule import StrategyPatternRule
from pattern_detector.domain.rules.struct_embedding_rule import StructEmbeddingRule
from pattern_detector.domain.rules.template_method_rule import TemplateMethodRule
from pattern_detector.domain.rules.unchecked_error_rule import UncheckedErrorRule
from pattern_detector.domain.rules.visitor_rule import VisitorPatternRule
from pattern_detector.domain.rules.worker_pool_rule import WorkerPoolRule

DEFAULT_RULES: list[PatternRule] = [
    # Creational (6)
    FunctionalOptionsRule(),
    BuilderPatternRule(),
    FactoryMethodRule(),
    AbstractFactoryRule(),
    SingletonPatternRule(),
    PrototypePatternRule(),

    # Structural (7)
    AdapterPatternRule(),
    DecoratorPatternRule(),
    FacadePatternRule(),
    CompositePatternRule(),
    ProxyPatternRule(),
    BridgePatternRule(),
    FlyweightPatternRule(),

    # Behavioral (11)
    StrategyPatternRule(),
    ObserverPatternRule(),
    CommandPatternRule(),
    TemplateMethodRule(),
    ChainOfResponsibilityRule(),
    IteratorPatternRule(),
    MediatorPatternRule(),
    MementoPatternRule(),
    VisitorPatternRule(),
    InterpreterPatternRule(),
    StatePatternRule(),

    # Go Concurrency & Idioms (8)
    PipelinePatternRule(),
    FanOutFanInRule(),
    WorkerPoolRule(),
    GeneratorPatternRule(),
    ContextPropagationRule(),
    ErrgroupConcurrencyRule(),
    StructEmbeddingRule(),
    CircularDependencyRule(),

    # SOLID, Clean Code & Safety (11)
    SingleResponsibilityRule(),
    InterfacePollutionRule(),
    OpenClosedPrincipleRule(),
    LiskovSubstitutionRule(),
    DependencyInversionRule(),
    LawOfDemeterRule(),
    HighCohesionLowCouplingRule(),
    KissRule(),
    DryRule(),
    GoroutineLeakRule(),
    UncheckedErrorRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    "FunctionalOptionsRule",
    "BuilderPatternRule",
    "FactoryMethodRule",
    "AbstractFactoryRule",
    "SingletonPatternRule",
    "PrototypePatternRule",
    "AdapterPatternRule",
    "DecoratorPatternRule",
    "FacadePatternRule",
    "CompositePatternRule",
    "ProxyPatternRule",
    "BridgePatternRule",
    "FlyweightPatternRule",
    "StrategyPatternRule",
    "ObserverPatternRule",
    "CommandPatternRule",
    "TemplateMethodRule",
    "ChainOfResponsibilityRule",
    "IteratorPatternRule",
    "MediatorPatternRule",
    "MementoPatternRule",
    "VisitorPatternRule",
    "InterpreterPatternRule",
    "StatePatternRule",
    "PipelinePatternRule",
    "FanOutFanInRule",
    "WorkerPoolRule",
    "GeneratorPatternRule",
    "ContextPropagationRule",
    "ErrgroupConcurrencyRule",
    "StructEmbeddingRule",
    "CircularDependencyRule",
    "SingleResponsibilityRule",
    "InterfacePollutionRule",
    "OpenClosedPrincipleRule",
    "LiskovSubstitutionRule",
    "DependencyInversionRule",
    "LawOfDemeterRule",
    "HighCohesionLowCouplingRule",
    "KissRule",
    "DryRule",
    "GoroutineLeakRule",
    "UncheckedErrorRule",
]

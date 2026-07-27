# ADR-001: Split Public Archive from Private Creator OS

**Status:** Accepted

**Date:** 2026-07-09

## Context

Early planning risked making `chlokat.frikshun.com` feel like an administrative publishing tool rather than Chloe's fan experience.

## Decision

The public ChloKat site is the searchable archive, news, release, and fan-exploration surface. Creator OS is a private FrikShun operations tool and may become a hosted creator product only through a later decision.

## Rationale and consequences

The split gives fans a coherent destination, protects private workflows, and lets operational tooling evolve separately. Approved artifacts cross the boundary; admin workflows do not. Two applications may share data, so schema ownership must remain coordinated.

## Alternatives considered

A single public/admin ChloKat application was rejected by the clarification.

Source: `frikshun_marketing/archives/chloe-katastrophe/workflows/chlokat_evil_plan_packet/chlokat_evil_plan/docs/architecture_clarification_2026-07-09.md`

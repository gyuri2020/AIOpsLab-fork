#!/usr/bin/env python3
"""Script to list all available problems in AIOpsLab with full details (no K8s required)."""

import json
import csv

# Task type descriptions and expected solution formats
TASK_TYPES = {
    "detection": {
        "description": "Detect anomalies in a deployed service",
        "expected_solution_format": 'str: "Yes" or "No"',
        "metric": "TTD (Time To Detect)",
    },
    "localization": {
        "description": "Identify the service(s) where the root cause of the fault lies",
        "expected_solution_format": "list[str]: list of faulty service names",
        "metric": "TTL (Time To Localize)",
    },
    "analysis": {
        "description": "Root cause analysis - identify system level and fault type",
        "expected_solution_format": 'dict: {"system_level": "...", "fault_type": "..."}',
        "metric": "TTA (Time To Analyze)",
        "system_levels": ["Hardware", "Operating System", "Virtualization", "Application"],
        "fault_types": ["Misconfiguration", "Code Defect", "Authentication Issue",
                       "Network/Storage Issue", "Operation Error", "Dependency Problem"],
    },
    "mitigation": {
        "description": "Mitigate/fix the detected anomaly",
        "expected_solution_format": "None (verified by system status check)",
        "metric": "TTM (Time To Mitigate)",
    },
}

# Full problem registry with detailed information
PROBLEMS = [
    # ============================================================================
    # K8s Target Port Misconfiguration - Social Network
    # ============================================================================
    {
        "id": "k8s_target_port-misconfig-detection-1",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "user-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-localization-1",
        "task": "localization",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "user-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '["user-service"]',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-analysis-1",
        "task": "analysis",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "user-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Misconfiguration"}',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-mitigation-1",
        "task": "mitigation",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "user-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Reset target port to 9090, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    # Variant 2: text-service
    {
        "id": "k8s_target_port-misconfig-detection-2",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "text-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-localization-2",
        "task": "localization",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "text-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '["text-service"]',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-analysis-2",
        "task": "analysis",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "text-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Misconfiguration"}',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-mitigation-2",
        "task": "mitigation",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "text-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Reset target port to 9090, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    # Variant 3: post-storage-service
    {
        "id": "k8s_target_port-misconfig-detection-3",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "post-storage-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-localization-3",
        "task": "localization",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "post-storage-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '["post-storage-service"]',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-analysis-3",
        "task": "analysis",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "post-storage-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Misconfiguration"}',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "k8s_target_port-misconfig-mitigation-3",
        "task": "mitigation",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "post-storage-service",
        "fault_type": "misconfig_k8s",
        "fault_description": "K8s service target port misconfiguration",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Reset target port to 9090, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },

    # ============================================================================
    # MongoDB Auth Missing - Hotel Reservation
    # ============================================================================
    {
        "id": "auth_miss_mongodb-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_missing",
        "fault_description": "MongoDB authentication credentials missing",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "auth_miss_mongodb-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_missing",
        "fault_description": "MongoDB authentication credentials missing",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["mongodb-rate"]',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "auth_miss_mongodb-analysis-1",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_missing",
        "fault_description": "MongoDB authentication credentials missing",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Authentication Issue"}',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "auth_miss_mongodb-mitigation-1",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_missing",
        "fault_description": "MongoDB authentication credentials missing",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Restore MongoDB authentication, all pods Running",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },

    # ============================================================================
    # MongoDB Auth Revoke - Hotel Reservation (mongodb-geo)
    # ============================================================================
    {
        "id": "revoke_auth_mongodb-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["mongodb-geo"]',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-analysis-1",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Authentication Issue"}',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-mitigation-1",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Restore MongoDB authentication, all pods Running",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    # Variant 2: mongodb-rate
    {
        "id": "revoke_auth_mongodb-detection-2",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-localization-2",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["mongodb-rate"]',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-analysis-2",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Authentication Issue"}',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "revoke_auth_mongodb-mitigation-2",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "auth_revoke",
        "fault_description": "MongoDB authentication revoked",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Restore MongoDB authentication, all pods Running",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },

    # ============================================================================
    # MongoDB User Unregistered - Hotel Reservation
    # ============================================================================
    {
        "id": "user_unregistered_mongodb-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["mongodb-geo"]',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-analysis-1",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Authentication Issue"}',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-mitigation-1",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-geo",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Re-register MongoDB user, all pods Running",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    # Variant 2: mongodb-rate
    {
        "id": "user_unregistered_mongodb-detection-2",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-localization-2",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["mongodb-rate"]',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-analysis-2",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Authentication Issue"}',
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },
    {
        "id": "user_unregistered_mongodb-mitigation-2",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb-rate",
        "fault_type": "user_unregistered",
        "fault_description": "MongoDB user unregistered/deleted",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Re-register MongoDB user, all pods Running",
        "system_level": "Application",
        "fault_category": "Authentication Issue",
    },

    # ============================================================================
    # App Misconfiguration - Hotel Reservation
    # ============================================================================
    {
        "id": "misconfig_app_hotel_res-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "frontend",
        "fault_type": "app_misconfig",
        "fault_description": "Application misconfiguration in frontend",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "misconfig_app_hotel_res-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "frontend",
        "fault_type": "app_misconfig",
        "fault_description": "Application misconfiguration in frontend",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["frontend"]',
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "misconfig_app_hotel_res-analysis-1",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "frontend",
        "fault_type": "app_misconfig",
        "fault_description": "Application misconfiguration in frontend",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Application", "fault_type": "Misconfiguration"}',
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "misconfig_app_hotel_res-mitigation-1",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "frontend",
        "fault_type": "app_misconfig",
        "fault_description": "Application misconfiguration in frontend",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Fix configuration, all pods Running",
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },

    # ============================================================================
    # Scale Pod to Zero - Social Network
    # ============================================================================
    {
        "id": "scale_pod_zero_social_net-detection-1",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "scale_pod_zero",
        "fault_description": "Pod scaled to zero replicas",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "scale_pod_zero_social_net-localization-1",
        "task": "localization",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "scale_pod_zero",
        "fault_description": "Pod scaled to zero replicas",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '["compose-post-service"]',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "scale_pod_zero_social_net-analysis-1",
        "task": "analysis",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "scale_pod_zero",
        "fault_description": "Pod scaled to zero replicas",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Operation Error"}',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "scale_pod_zero_social_net-mitigation-1",
        "task": "mitigation",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "scale_pod_zero",
        "fault_description": "Pod scaled to zero replicas",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Scale pod back to 1+, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },

    # ============================================================================
    # Assign to Non-Existent Node - Social Network
    # ============================================================================
    {
        "id": "assign_to_non_existent_node_social_net-detection-1",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "assign_non_existent_node",
        "fault_description": "Pod assigned to non-existent node",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "assign_to_non_existent_node_social_net-localization-1",
        "task": "localization",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "assign_non_existent_node",
        "fault_description": "Pod assigned to non-existent node",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '["compose-post-service"]',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "assign_to_non_existent_node_social_net-analysis-1",
        "task": "analysis",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "assign_non_existent_node",
        "fault_description": "Pod assigned to non-existent node",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Misconfiguration"}',
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "assign_to_non_existent_node_social_net-mitigation-1",
        "task": "mitigation",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "compose-post-service",
        "fault_type": "assign_non_existent_node",
        "fault_description": "Pod assigned to non-existent node",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "Remove invalid node selector, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Misconfiguration",
    },

    # ============================================================================
    # Chaos Mesh Faults - Hotel Reservation
    # ============================================================================
    {
        "id": "container_kill-detection",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "container_kill",
        "fault_description": "Container killed via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "container_kill-localization",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "container_kill",
        "fault_description": "Container killed via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["user"]',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "pod_failure_hotel_res-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "pod_failure",
        "fault_description": "Pod failure injected via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "pod_failure_hotel_res-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "pod_failure",
        "fault_description": "Pod failure injected via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["user"]',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "pod_kill_hotel_res-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "pod_kill",
        "fault_description": "Pod killed via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "pod_kill_hotel_res-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "pod_kill",
        "fault_description": "Pod killed via Chaos Mesh",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["user"]',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "network_loss_hotel_res-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "network_loss",
        "fault_description": "Network packet loss injected",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Operating System",
        "fault_category": "Network/Storage Issue",
    },
    {
        "id": "network_loss_hotel_res-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "network_loss",
        "fault_description": "Network packet loss injected",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["user"]',
        "system_level": "Operating System",
        "fault_category": "Network/Storage Issue",
    },
    {
        "id": "network_delay_hotel_res-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "network_delay",
        "fault_description": "Network delay/latency injected",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Operating System",
        "fault_category": "Network/Storage Issue",
    },
    {
        "id": "network_delay_hotel_res-localization-1",
        "task": "localization",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "user",
        "fault_type": "network_delay",
        "fault_description": "Network delay/latency injected",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '["user"]',
        "system_level": "Operating System",
        "fault_category": "Network/Storage Issue",
    },

    # ============================================================================
    # No-Op (Baseline) - No fault injected
    # ============================================================================
    {
        "id": "noop_detection_hotel_reservation-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "N/A",
        "fault_type": "noop",
        "fault_description": "No fault injected (baseline test)",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "No",
        "system_level": "N/A",
        "fault_category": "N/A",
    },
    {
        "id": "noop_detection_social_network-1",
        "task": "detection",
        "app": "Social Network",
        "namespace": "social-network",
        "faulty_service": "N/A",
        "fault_type": "noop",
        "fault_description": "No fault injected (baseline test)",
        "workload": "socialNetwork/wrk2/scripts/social-network/compose-post.lua",
        "expected_solution": "No",
        "system_level": "N/A",
        "fault_category": "N/A",
    },
    {
        "id": "noop_detection_astronomy_shop-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "N/A",
        "fault_type": "noop",
        "fault_description": "No fault injected (baseline test)",
        "workload": "N/A",
        "expected_solution": "No",
        "system_level": "N/A",
        "fault_category": "N/A",
    },

    # ============================================================================
    # Astronomy Shop (OpenTelemetry Demo) - Feature Flag Failures
    # ============================================================================
    {
        "id": "astronomy_shop_ad_service_failure-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "feature_flag_failure",
        "fault_description": "Ad service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_ad_service_failure-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "feature_flag_failure",
        "fault_description": "Ad service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["ad-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_ad_service_high_cpu-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "high_cpu",
        "fault_description": "Ad service high CPU usage via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_ad_service_high_cpu-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "high_cpu",
        "fault_description": "Ad service high CPU usage via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["ad-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_ad_service_manual_gc-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "manual_gc",
        "fault_description": "Ad service manual garbage collection issue",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_ad_service_manual_gc-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "ad-service",
        "fault_type": "manual_gc",
        "fault_description": "Ad service manual garbage collection issue",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["ad-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_cart_service_failure-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "cart-service",
        "fault_type": "service_failure",
        "fault_description": "Cart service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_cart_service_failure-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "cart-service",
        "fault_type": "service_failure",
        "fault_description": "Cart service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["cart-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_image_slow_load-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "image-provider",
        "fault_type": "slow_load",
        "fault_description": "Image provider slow loading",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_image_slow_load-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "image-provider",
        "fault_type": "slow_load",
        "fault_description": "Image provider slow loading",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["image-provider"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_kafka_queue_problems-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "kafka",
        "fault_type": "queue_problems",
        "fault_description": "Kafka queue processing issues",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Dependency Problem",
    },
    {
        "id": "astronomy_shop_kafka_queue_problems-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "kafka",
        "fault_type": "queue_problems",
        "fault_description": "Kafka queue processing issues",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["kafka"]',
        "system_level": "Application",
        "fault_category": "Dependency Problem",
    },
    {
        "id": "astronomy_shop_kafka_queue_problems-mitigation-1",
        "task": "mitigation",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "kafka",
        "fault_type": "queue_problems",
        "fault_description": "Kafka queue processing issues",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Fix Kafka queue, all pods Running",
        "system_level": "Application",
        "fault_category": "Dependency Problem",
    },
    {
        "id": "astronomy_shop_loadgenerator_flood_homepage-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "loadgenerator",
        "fault_type": "flood_homepage",
        "fault_description": "Load generator flooding homepage",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Operation Error",
    },
    {
        "id": "astronomy_shop_loadgenerator_flood_homepage-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "loadgenerator",
        "fault_type": "flood_homepage",
        "fault_description": "Load generator flooding homepage",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["loadgenerator"]',
        "system_level": "Application",
        "fault_category": "Operation Error",
    },
    {
        "id": "astronomy_shop_payment_service_failure-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "payment-service",
        "fault_type": "service_failure",
        "fault_description": "Payment service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_payment_service_failure-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "payment-service",
        "fault_type": "service_failure",
        "fault_description": "Payment service failure via feature flag",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["payment-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_payment_service_unreachable-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "payment-service",
        "fault_type": "unreachable",
        "fault_description": "Payment service unreachable",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Network/Storage Issue",
    },
    {
        "id": "astronomy_shop_payment_service_unreachable-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "payment-service",
        "fault_type": "unreachable",
        "fault_description": "Payment service unreachable",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["payment-service"]',
        "system_level": "Application",
        "fault_category": "Network/Storage Issue",
    },
    {
        "id": "astronomy_shop_product_catalog_service_failure-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "product-catalog-service",
        "fault_type": "service_failure",
        "fault_description": "Product catalog service failure",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_product_catalog_service_failure-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "product-catalog-service",
        "fault_type": "service_failure",
        "fault_description": "Product catalog service failure",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["product-catalog-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_recommendation_service_cache_failure-detection-1",
        "task": "detection",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "recommendation-service",
        "fault_type": "cache_failure",
        "fault_description": "Recommendation service cache failure",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Code Defect",
    },
    {
        "id": "astronomy_shop_recommendation_service_cache_failure-localization-1",
        "task": "localization",
        "app": "Astronomy Shop",
        "namespace": "astronomy-shop",
        "faulty_service": "recommendation-service",
        "fault_type": "cache_failure",
        "fault_description": "Recommendation service cache failure",
        "workload": "OpenTelemetry Demo workload",
        "expected_solution": '["recommendation-service"]',
        "system_level": "Application",
        "fault_category": "Code Defect",
    },

    # ============================================================================
    # Redeploy Without PV - Hotel Reservation
    # ============================================================================
    {
        "id": "redeploy_without_PV-detection-1",
        "task": "detection",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb",
        "fault_type": "redeploy_without_pv",
        "fault_description": "Namespace redeployed without deleting PersistentVolume",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Yes",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "redeploy_without_PV-analysis-1",
        "task": "analysis",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb",
        "fault_type": "redeploy_without_pv",
        "fault_description": "Namespace redeployed without deleting PersistentVolume",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": '{"system_level": "Virtualization", "fault_type": "Operation Error"}',
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },
    {
        "id": "redeploy_without_PV-mitigation-1",
        "task": "mitigation",
        "app": "Hotel Reservation",
        "namespace": "hotel-reserv",
        "faulty_service": "mongodb",
        "fault_type": "redeploy_without_pv",
        "fault_description": "Namespace redeployed without deleting PersistentVolume",
        "workload": "hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
        "expected_solution": "Delete old PV and recreate, all pods Running",
        "system_level": "Virtualization",
        "fault_category": "Operation Error",
    },

    # ============================================================================
    # Wrong Bin Usage
    # ============================================================================
    {
        "id": "wrong_bin_usage-detection-1",
        "task": "detection",
        "app": "General",
        "namespace": "default",
        "faulty_service": "app",
        "fault_type": "wrong_bin_usage",
        "fault_description": "Wrong binary being used in container",
        "workload": "N/A",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "wrong_bin_usage-localization-1",
        "task": "localization",
        "app": "General",
        "namespace": "default",
        "faulty_service": "app",
        "fault_type": "wrong_bin_usage",
        "fault_description": "Wrong binary being used in container",
        "workload": "N/A",
        "expected_solution": '["app"]',
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "wrong_bin_usage-analysis-1",
        "task": "analysis",
        "app": "General",
        "namespace": "default",
        "faulty_service": "app",
        "fault_type": "wrong_bin_usage",
        "fault_description": "Wrong binary being used in container",
        "workload": "N/A",
        "expected_solution": '{"system_level": "Application", "fault_type": "Misconfiguration"}',
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },
    {
        "id": "wrong_bin_usage-mitigation-1",
        "task": "mitigation",
        "app": "General",
        "namespace": "default",
        "faulty_service": "app",
        "fault_type": "wrong_bin_usage",
        "fault_description": "Wrong binary being used in container",
        "workload": "N/A",
        "expected_solution": "Fix binary path, all pods Running",
        "system_level": "Application",
        "fault_category": "Misconfiguration",
    },

    # ============================================================================
    # Flower (Federated Learning) - Docker-based
    # ============================================================================
    {
        "id": "flower_node_stop-detection",
        "task": "detection",
        "app": "Flower (FL)",
        "namespace": "docker",
        "faulty_service": "node",
        "fault_type": "node_stop",
        "fault_description": "Federated learning node stopped",
        "workload": "Flower FL workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Operation Error",
        "deployment": "docker",
    },
    {
        "id": "flower_model_misconfig-detection",
        "task": "detection",
        "app": "Flower (FL)",
        "namespace": "docker",
        "faulty_service": "model",
        "fault_type": "model_misconfig",
        "fault_description": "Federated learning model misconfiguration",
        "workload": "Flower FL workload",
        "expected_solution": "Yes",
        "system_level": "Application",
        "fault_category": "Misconfiguration",
        "deployment": "docker",
    },
]

# Add default deployment type
for p in PROBLEMS:
    if "deployment" not in p:
        p["deployment"] = "k8s"


def save_to_json(problems, filename="problems.json"):
    """Save problems to JSON file."""
    output = {
        "task_types": TASK_TYPES,
        "problems": problems,
        "summary": {
            "total": len(problems),
            "by_task": {},
            "by_app": {},
        }
    }

    for task in ["detection", "localization", "analysis", "mitigation"]:
        output["summary"]["by_task"][task] = len([p for p in problems if p["task"] == task])

    for app in sorted(set(p["app"] for p in problems)):
        output["summary"]["by_app"][app] = len([p for p in problems if p["app"] == app])

    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved to {filename}")


def save_to_csv(problems, filename="problems.csv"):
    """Save problems to CSV file."""
    fieldnames = [
        "id", "task", "app", "namespace", "faulty_service",
        "fault_type", "fault_description", "workload",
        "expected_solution", "system_level", "fault_category", "deployment"
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(problems)
    print(f"Saved to {filename}")


def save_to_txt(problems, filename="problems.txt"):
    """Save problems to formatted text file."""
    with open(filename, "w") as f:
        f.write("=" * 100 + "\n")
        f.write("AIOpsLab Problem Registry - Complete Details\n")
        f.write("=" * 100 + "\n\n")

        # Task type descriptions
        f.write("TASK TYPES\n")
        f.write("-" * 100 + "\n\n")
        for task, info in TASK_TYPES.items():
            f.write(f"{task.upper()}:\n")
            f.write(f"  Description: {info['description']}\n")
            f.write(f"  Expected Solution Format: {info['expected_solution_format']}\n")
            f.write(f"  Metric: {info['metric']}\n")
            if "system_levels" in info:
                f.write(f"  System Levels: {', '.join(info['system_levels'])}\n")
            if "fault_types" in info:
                f.write(f"  Fault Types: {', '.join(info['fault_types'])}\n")
            f.write("\n")

        # Problems grouped by task type
        task_types = ["detection", "localization", "analysis", "mitigation"]

        for task_type in task_types:
            task_problems = [p for p in problems if p["task"] == task_type]
            if not task_problems:
                continue

            f.write("\n" + "=" * 100 + "\n")
            f.write(f"{task_type.upper()} PROBLEMS ({len(task_problems)})\n")
            f.write("=" * 100 + "\n\n")

            for i, p in enumerate(task_problems, 1):
                deploy_icon = "[Docker]" if p["deployment"] == "docker" else "[K8s]"
                f.write(f"{i:3}. {deploy_icon} {p['id']}\n")
                f.write(f"     ├─ Application:       {p['app']}\n")
                f.write(f"     ├─ Namespace:         {p['namespace']}\n")
                f.write(f"     ├─ Faulty Service:    {p['faulty_service']}\n")
                f.write(f"     ├─ Fault Type:        {p['fault_type']}\n")
                f.write(f"     ├─ Fault Description: {p['fault_description']}\n")
                f.write(f"     ├─ Workload:          {p['workload']}\n")
                f.write(f"     ├─ Expected Solution: {p['expected_solution']}\n")
                f.write(f"     ├─ System Level:      {p['system_level']}\n")
                f.write(f"     └─ Fault Category:    {p['fault_category']}\n")
                f.write("\n")

        # Summary
        f.write("\n" + "=" * 100 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Total Problems: {len(problems)}\n\n")

        f.write("By Task Type:\n")
        for task_type in task_types:
            count = len([p for p in problems if p["task"] == task_type])
            f.write(f"  - {task_type.capitalize()}: {count}\n")

        f.write("\nBy Application:\n")
        apps = sorted(set(p["app"] for p in problems))
        for app in apps:
            count = len([p for p in problems if p["app"] == app])
            f.write(f"  - {app}: {count}\n")

        f.write("\nBy System Level:\n")
        levels = sorted(set(p["system_level"] for p in problems))
        for level in levels:
            count = len([p for p in problems if p["system_level"] == level])
            f.write(f"  - {level}: {count}\n")

        f.write("\nBy Fault Category:\n")
        categories = sorted(set(p["fault_category"] for p in problems))
        for cat in categories:
            count = len([p for p in problems if p["fault_category"] == cat])
            f.write(f"  - {cat}: {count}\n")

        f.write("\nBy Deployment:\n")
        f.write(f"  - Kubernetes: {len([p for p in problems if p['deployment'] == 'k8s'])}\n")
        f.write(f"  - Docker: {len([p for p in problems if p['deployment'] == 'docker'])}\n")

    print(f"Saved to {filename}")


def print_summary(problems):
    """Print summary to console."""
    print("=" * 70)
    print("AIOpsLab Problem Registry")
    print("=" * 70)
    print(f"\nTotal: {len(problems)} problems\n")

    print("By Task Type:")
    for task in ["detection", "localization", "analysis", "mitigation"]:
        count = len([p for p in problems if p["task"] == task])
        print(f"  - {task.capitalize()}: {count}")

    print("\nBy Application:")
    apps = sorted(set(p["app"] for p in problems))
    for app in apps:
        count = len([p for p in problems if p["app"] == app])
        print(f"  - {app}: {count}")

    print("\nBy Fault Category:")
    categories = sorted(set(p["fault_category"] for p in problems))
    for cat in categories:
        count = len([p for p in problems if p["fault_category"] == cat])
        print(f"  - {cat}: {count}")


def main():
    print("Generating comprehensive problem list...\n")

    # Save to all formats
    save_to_json(PROBLEMS, "problems.json")
    save_to_csv(PROBLEMS, "problems.csv")
    save_to_txt(PROBLEMS, "problems.txt")

    print()
    print_summary(PROBLEMS)

    print("\n" + "=" * 70)
    print("Files created:")
    print("  - problems.json (machine-readable with task type info)")
    print("  - problems.csv  (spreadsheet-friendly)")
    print("  - problems.txt  (human-readable detailed report)")
    print("=" * 70)


if __name__ == "__main__":
    main()

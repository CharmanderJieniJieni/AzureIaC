from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource.policy.models import PolicyDefinition

from Model.PolicyConfig import PolicyConfig
from Util import Session

import json, subprocess

class PolicyManagerException(Exception):
    pass

class PolicyManager:
    """Manage Azure Policy related events"""

    def __init__(self, session: Session):
        self.session = session
        self.credentials = session.credentials
        self.policy_client = None

    def create_policy_definition(self, policy_config: PolicyConfig):
        """define policy at subscription scope"""

        # DeployIfNotExist is not supported by SDK. see ref: https://github.com/Azure/azure-policy/issues/20
        # Use CLI for deployIfNotExist instead
        self.policy_client = PolicyClient(
            self.credentials, policy_config.subscription_id
        )
        policy_definition = PolicyDefinition(
            mode="All",
            display_name=policy_config.policy_display_name,
            description=policy_config.policy_description,
            policy_rule=policy_config.policy_rule,
        )
        policy_effect = policy_config.policy_rule.get("then").get("effect").lower()
        if policy_effect == "deployifnotexists":
            return self.__policy_definition_cli(policy_config)
        else:
            return self.policy_client.policy_definitions.create_or_update(
                policy_config.policy_name, policy_definition
            )

    def clear_subscription_policy_definitions(
        self, subscription_id: str, policy_configs: [PolicyConfig]
    ):
        self.policy_client = PolicyClient(self.credentials, subscription_id)
        current_policy_definitions = self.policy_client.policy_definitions.list()
        desired_defintion_names = []
        for desired_policy in policy_configs:
            desired_defintion_names.append(desired_policy.policy_name)
        for policy_definition in current_policy_definitions:
            if policy_definition.policy_type == "Custom":
                if policy_definition.name not in desired_defintion_names:
                    self.__delete_policy_definition(
                        subscription_id, policy_definition.name
                    )

    def __delete_policy_definition(self, subscription_id: str, policy_name: str):
        self.policy_client = PolicyClient(self.credentials, subscription_id)
        policy_assignment_list = self.__list_policy_assignments(subscription_id)
        policy_definition_id = self.policy_client.policy_definitions.get(policy_name).id
        for policy_assignment in policy_assignment_list:
            if policy_assignment.policy_definition_id == policy_definition_id:
                self.policy_client.policy_assignments.delete_by_id(policy_assignment.id)
        self.policy_client.policy_definitions.delete(policy_name)

    def __list_policy_assignments(self, subscription_id: str):
        self.policy_client = PolicyClient(self.credentials, subscription_id)
        return self.policy_client.policy_assignments.list()

    def __policy_definition_cli(self, policy_configs: PolicyConfig):
        self.session.az_cli_login()
        policy_name = policy_configs.policy_name
        policy_display_name = policy_configs.policy_display_name or ""
        policy_discription = policy_configs.policy_description or ""
        policy_rule_path = policy_configs.policy_rule_path
        policy_params_path = policy_configs.policy_params_path
        if policy_params_path:
            job = subprocess.run(
                [
                    "az",
                    "policy",
                    "definition",
                    "create",
                    "--name",
                    policy_name,
                    "--display-name",
                    policy_display_name,
                    "--rules",
                    policy_rule_path,
                    "--params",
                    policy_params_path,
                ],
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
            )
        else:
            job = subprocess.run(
                [
                    "az",
                    "policy",
                    "definition",
                    "create",
                    "--name",
                    policy_name,
                    "--display-name",
                    policy_display_name,
                    "--rules",
                    policy_rule_path,
                ],
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
            )

        job.check_returncode()
       
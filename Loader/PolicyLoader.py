from Pipeline.Model.PolicyConfig import PolicyConfig
import yaml, json


class PolicyLoader:
    @classmethod
    def load_policy_config(cls, config_path: str):
        subscription_policy_config = []
        with open(config_path, "r") as stream:
            config_raw = yaml.safe_load(stream)

        subscription_policy_configs = config_raw.get("Subscriptions")
        policy_definition_configs = config_raw.get("PolicyDefinitions")
        for (
            subscription_name,
            subscription_details,
        ) in subscription_policy_configs.items():
            subscription_id = subscription_details.get("SubscriptionId")
            policies = subscription_details.get("Policies")
            if policies:
                for policy in policies:
                    policy_definition_name = policy.get("DefinitionName")
                    policy_definition_config = policy_definition_configs.get(
                        policy_definition_name
                    )
                    policy_display_name = policy_definition_config.get("DisplayName")
                    policy_description = policy_definition_config.get("Description")
                    policy_rule_path = policy_definition_config.get("RulePath")
                    policy_params_path = policy_definition_config.get("ParamsPath")
                    policy_rule = cls.__load_json_from_path(policy_rule_path)
                    if policy_params_path:
                        policy_params = cls.__load_json_from_path(policy_params_path)
                    else:
                        policy_params = None
                    policy_config_model = PolicyConfig(
                        subscription_id,
                        policy_definition_name,
                        policy_display_name,
                        policy_rule,
                        policy_params,
                        policy_description,
                        policy_rule_path,
                        policy_params_path
                    )
                    subscription_policy_config.append(policy_config_model)
            else: 
                policy_config_model = PolicyConfig(subscription_id=subscription_id)
            subscription_policy_config.append(policy_config_model)

        return subscription_policy_config

    @classmethod
    def __load_json_from_path(cls, path: str):
        with open(path) as file:
            return json.load(file)

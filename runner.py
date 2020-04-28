from Manager.PolicyManager import PolicyManager
from Loader.PolicyLoader import PolicyLoader
from Model.PolicyConfig import PolicyConfig
from Util.Session import Session
import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--option", help="option of runner, e.g. policy_definition")
    parser.add_argument("--policy-config-path", help="path to policy rule")

    args = parser.parse_args()
    option = args.option
    policy_config_path = args.policy_config_path

    if option == "policy_definition":
        policy_config_models = PolicyLoader.load_policy_config(policy_config_path)
        clean_policy_definitions(policy_config_models)
        for policy_config in policy_config_models:
            if policy_config.policy_name:
                define_policy(policy_config)


def define_policy(policy_config: PolicyConfig):
    session = Session()
    subscription_id = policy_config.subscription_id
    policy_manager = PolicyManager(session)
    result = policy_manager.create_policy_definition(policy_config)


def clean_policy_definitions(policy_configs: [PolicyConfig]):
    session = Session()
    subscription_id = policy_configs[0].subscription_id
    policy_manager = PolicyManager(session)
    result = policy_manager.clear_subscription_policy_definitions(
        subscription_id, policy_configs
    )


if __name__ == "__main__":
    run()

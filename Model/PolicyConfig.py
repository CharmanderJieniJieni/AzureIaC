class PolicyConfig:
    def __init__(
        self,
        subscription_id: str,
        policy_name: str = None,
        policy_display_name: str = None,
        policy_rule: dict = None,
        policy_params: dict = None,
        policy_description: str = None,
        policy_rule_path: str = None,
        policy_params_path: str = None
    ):
        self.__subscription_id = subscription_id
        self.__policy_name = policy_name
        self.__policy_display_name = policy_display_name
        self.__policy_rule = policy_rule
        self.__policy_params = policy_params
        self.__policy_description = policy_description
        self.__policy_rule_path = policy_rule_path
        self.__policy_params_path = policy_params_path

    @property
    def subscription_id(self):
        return self.__subscription_id

    @property
    def policy_name(self):
        return self.__policy_name

    @property
    def policy_display_name(self):
        return self.__policy_display_name

    @property
    def policy_rule(self):
        return self.__policy_rule

    @property
    def policy_params(self):
        return self.__policy_params

    @property
    def policy_description(self):
        return self.__policy_description

    @property
    def policy_rule_path(self):
        return self.__policy_rule_path
    
    @property
    def policy_params_path(self):
        return self.__policy_params_path
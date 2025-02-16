def evaluate_rule(email, rule):
    """Evaluates whether a given email matches a rule."""
    conditions_met = []
    for condition in rule['conditions']:
        email_value = email.get(condition['field'], '')
        if condition['operator'] == 'contains' and condition['value'] in email_value:
            conditions_met.append(True)
        elif condition['operator'] == 'does_not_contain' and condition['value'] not in email_value:
            conditions_met.append(True)
        elif condition['operator'] == 'equals' and email_value == condition['value']:
            conditions_met.append(True)
        elif condition['operator'] == 'does_not_equal' and email_value != condition['value']:
            conditions_met.append(True)
        else:
            conditions_met.append(False)

    return all(conditions_met) if rule['predicate'] == 'All' else any(conditions_met)

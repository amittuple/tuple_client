def first_it_come_check(input_check):

    if input_check == [u'send']:
        return 'Select Platform like: facebook or mailchimp or google sheet'
    if input_check==[u'help']:
        return "you can type cltv = high churn = high or cltv < 1000 in tuple_mia"

    if input_check==[u'filter']:
        return "Choose Filter like: Profile or Predictions"

    if input_check==[u'predictions']:
        return "Choose Levels like: Churn or CLTV or High Converter or Value or Engement"

    if input_check==[u'profile']:
        return "Choose Levels like: Name or Age or Country or email"

    if input_check==[u'country']:
        return 'Enter Value (Country takes names)'

    if input_check==[u'cltv']:

        return "Enter Value (CLTV takes numeric values)"

    if input_check==[u'churn']:
        return "Enter Value (CHURN takes numeric values)"

    if input_check==[u'name']:
        return "Enter Value (NAME takes takes string)"

    if input_check==[u'age']:
        return "Enter Value(AGE takes takes numeric values)"

    if input_check==[u'gender']:
        return "Enter Value (NAME takes takes only M or F )"
    return 'amit_bot'
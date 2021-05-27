message_info = {} # holds relevant info for each user session such as the message ID of their embed results and timer
# will have format {user_id : [message_id, expiry_timer, current_index]}
user_results = {} # holds the results from the webscrape for a particular user
# format: {user_id: [[]]}
# each column has format [name, price, reviews, link]
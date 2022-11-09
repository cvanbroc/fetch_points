# webserver.py

from flask import Flask, request, jsonify

webserver = Flask(__name__)

transactions = []

@webserver.get("/transactions")
def get_transactions():
    return jsonify(transactions)

@webserver.get("/points")
def get_points():
    points = {}
    # put payer and points values of each transaction in a dictionary
    for i in transactions:
        key = i["payer"]
        value = i["points"]
        # check if key already exists in dictionary
        if key in points.keys():
            # if there is a match - sum the points instead of overwriting the key,value pair
            points[key] = points.get(key) + value
        else:
            # if there is not a match - just add the new key,value pair to the dictionary
            points.update({key: value})
    # return the dictionary
    return jsonify(points)

@webserver.post("/transactions")
def add_transaction():
    if request.is_json:
        transactionJSON = request.get_json()
        transactions.append(transactionJSON)
        return transactionJSON, 201
    return {"error": "Request is not JSON"}, 415

# helper function to run quick verification on whether point spend should be allowed
# returns true if there are enough transaction points to be spent, false otherwise
def _check_point_spend(spendPointsJSON):
    spendPoints = spendPointsJSON["points"]
    if spendPoints < 0:
        return False
    totalPoints = 0
    for i in transactions:
        # ignore any negative point values, only count positive ones
        if i["points"] > 0:
            totalPoints += i["points"]
            if totalPoints >= spendPoints:
                return True
    return False

def _update_spent_dict(payers, key, spendPoints):
    if key in payers.keys():
        payers[key] = payers.get(key) - spendPoints
    else:
        payers.update({key: -abs(spendPoints)})
    
@webserver.patch("/points")
def spend_points():
    if request.is_json:
        spendPointsJSON = request.get_json()

        if _check_point_spend(spendPointsJSON):
        # if there are enough points in the account to justify the spend, then adjust transactions and 'spend' points
            payers = {}
            # sort the list of transactions basted on timestamp
            transactions.sort(key=lambda x: x["timestamp"])
            # spend points, our list is sorted so we can just spend in order
            for i in transactions:

                    if (i["points"] >= spendPointsJSON["points"]):
                        # case where request is satisfied with part of a transaction's point total 
                        spentPoints = spendPointsJSON["points"]
                        _update_spent_dict(payers, i["payer"], spentPoints)

                        # update transaction to record some points used
                        i["points"] -= spentPoints

                        # can return from this case as there are no more points left on the request
                        spent  = []
                        # convert dictionary to proper display form for user
                        for key,value in payers.items():
                            if value != 0:
                                spent.append({"payer": key, "points": value})
                        return jsonify(spent)
                    else:
                        # case where request uses all of a transaction's point total
                        spentPoints = i["points"] 
                        _update_spent_dict(payers, i["payer"], spentPoints) 

                        # update request points
                        spendPointsJSON["points"] -= i["points"]
                        # update transaction to show all points used
                        i["points"] = 0
                        
        else:
            return {"error": "The requested point spend is not allowed"}, 422
    else:
        return {"error": "Reqeust is not JSON"}, 415


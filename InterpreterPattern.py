import json

import requests
# AbstractExpression class
class AbstractExpression(object):

    def interpret(self, context):
        pass
#integers Expression class
class IntegerExpression(AbstractExpression):

    def interpret(self, context):
        var = context.split("=")
        #reslove embeded
        if len(var)==2:
            var1= var.split("(")
            if len(var1) == 1:
                return int(var[0])
            else:
                #recursion
                int_var = self.interpret(var1)



    def interpret1(self, context):
        var = context.split("=")
        url = 'https://api.coinlore.net/api/ticker/?id='
        var = context.split("=")
        coin_id = var[1]
        url=url+coin_id
        resp = requests.get(url=url)
        return resp

    def ADD(self, context1,context2):
        int_var1 = self.interpret(context1)
        int_var2 = self.interpret(context2)
        return int_var1+int_var2

    def MULT(self, context1,context2):
        int_var1 = self.interpret(context1)
        int_var2 = self.interpret(context2)
        return int_var1*int_var2

    def TSUPPLY(self, context1):
        id = self.interpret(context1)
        coin = self.get_coin_dict[id]
        if coin:
            url = 'https://api.coinlore.net/api/ticker/?id='+str(coin.id)
            resp = requests.get(url=url)
            data = resp.json()
            res =data["data"].tsupply
            return res.tsupply
        else:
            res= []
            return res

    def RANK(self, context1):
        id = self.interpret(context1)
        coin = self.get_coin_dict[id]
        if coin:
            url = 'https://api.coinlore.net/api/ticker/?id='+str(coin.id)
            resp = requests.get(url=url)
            data = resp.json()
            res =data["data"].rank
            return res.rank
        else:
            res= []
            return res

    def get_coin_dict(self):
        url = 'https://api.coinlore.net/api/tickers/'
        resp = requests.get(url=url)
        data = resp.json()
        coin_dict = data["data"]
        return coin_dict


if __name__ == "__main__":
    IntegerExpression().interpret("x=5")
    IntegerExpression().interpret1("coin_id=90")


# -*- coding: utf-8 -*-

from lib import pybitflyer

if __name__ == '__main__':
  api = pybitflyer.API()
  board = api.board(product_code="BTC_JPY")
  print(board)


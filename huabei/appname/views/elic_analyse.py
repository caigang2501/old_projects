import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import request, jsonify,Blueprint

from mid_long.Medium_long_term_forecast import main_mdl_forecast
from mid_long.trading_strategy.consult import MarkRubinstein_Bargain_Model
from mid_long.trading_strategy.bidding import Mid_Long_Term_Transactions
from product_elic.Forecasting import main
from product_elic.Strategy import Spot_Quotation
from service_marcket.ganshu import main as ganshu_main
from service_marcket.guizhou.tiaoping import main as guizhou_main
from service_marcket.guizhou.tiaofeng import Depth_peak_regulation
from service_marcket.mengxi import main as mengxi_main
from tools import net
import logging

bp = Blueprint("main", __name__)

@bp.route("/test_get", methods=['GET'])
def test_get():
    return jsonify(1)

@bp.route("/mid_long", methods=['POST'])
def mid_long():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = main_mdl_forecast.main(path)
    return jsonify(list(result))
@bp.route("/mid_long/consult", methods=['POST'])
def mid_long_consult():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = MarkRubinstein_Bargain_Model.main(path)
    return jsonify(float(result))

# transaction
@bp.route("/mid_long/bidding", methods=['POST'])
def mid_long_bidding():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = Mid_Long_Term_Transactions.main(path)
    return jsonify(result)

@bp.route("/product", methods=['POST'])
def product():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = main.main(path)
    return jsonify(list(result))

@bp.route("/product/stratege", methods=['POST'])
def product_stratege():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = Spot_Quotation.spot(path)
    return jsonify(result)

@bp.route("/service_marcket/ganshu", methods=['POST'])
def ganshu():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = ganshu_main.main(path)
    return jsonify(list(result))

@bp.route("/service_marcket/guizhou", methods=['POST'])
def guizhou():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = guizhou_main.main(path)
    return jsonify(list(result))

@bp.route("/service_marcket/guizhou/tiaofeng", methods=['POST'])
def guizhou_tiaofeng():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = Depth_peak_regulation.midlong(path)
    return jsonify(list(result))

@bp.route("/service_marcket/mengxi", methods=['POST'])
def mengxi():
    url = request.get_json()['path']
    path = net.get_excel(url)
    result = mengxi_main.main(path)
    return jsonify(list(result))

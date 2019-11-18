from flask import Blueprint, request
from service import report_service


report_blueprint = Blueprint('report', __name__, url_prefix='/report')


@report_blueprint.route('/<string:unique_identifier>', methods=['GET'])
def report(unique_identifier: str):
    if request.method == 'GET':
        success: bool = report_service.report_asset_for_maintenance(unique_identifier)
        if success:
            # return success page
            return '200'
        else:
            # return failed page because asset was not found
            return '404'

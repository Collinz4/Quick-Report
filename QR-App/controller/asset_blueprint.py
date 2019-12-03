from flask import Blueprint, render_template, g, redirect, url_for, session, request
from service import asset_service
from models.models import Asset


asset_blueprint = Blueprint('assets', __name__, url_prefix='/assets')


@asset_blueprint.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@asset_blueprint.route('/', methods=['GET'])
def assets():
    if g.user:
        assets: [Asset] = asset_service.get_user_assets(g.user)
        return render_template('assets.html', assets=assets)
    else:
        return redirect(url_for('/.sign_in'))


@asset_blueprint.route('/<int:asset_id>', methods=['GET'])
def specific_asset(asset_id: int):
    if g.user:
        asset: Asset = asset_service.get_specific_user_asset(g.user, asset_id)
        return render_template('details_of_single_asset.html', asset=asset)
    else:
        return redirect(url_for('/.sign_in'))


@asset_blueprint.route('/edit/<int:asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id: int):
    if request.method == 'GET':
        if g.user:
            asset: Asset = asset_service.get_specific_user_asset(g.user, asset_id)
            return render_template('edit_single_asset_form.html', asset=asset)
        else:
            return redirect(url_for('.sign_in'))
    elif request.method == 'POST':
        if g.user:
            asset_service.update_specific_asset(
                g.user,
                asset_id,
                asset=Asset(
                    id=asset_id,
                    appliance=request.form.get('appliance'),
                    building=request.form.get('building'),
                    roomNumber=request.form.get('roomNumber'),
                    serviceRequired=False if request.form.get('serviceRequired') == 'False' else True
                )
            )
            asset: Asset = asset_service.get_specific_user_asset(g.user, asset_id)
            return render_template('edit_single_asset_form.html', asset=asset)


@asset_blueprint.route('/remove/<int:asset_id>', methods=['POST'])
def remove_asset(asset_id: int):
    if g.user:
        asset_service.remove_specific_asset(g.user, asset_id)
        return redirect(url_for('.assets'))
    else:
        return redirect(url_for('.sign_in'))


@asset_blueprint.route('/create', methods=['GET', 'POST'])
def create_asset():
    if g.user:
        if request.method == 'POST':
            asset = Asset(
                building=request.form.get('building'),
                roomNumber=request.form.get('roomNumber'),
                appliance=request.form.get('appliance'),
                serviceRequired=False
            )
            asset_service.create_asset(g.user, asset)
            return redirect(url_for('.assets'))
        elif request.method == 'GET':
            return render_template('create_asset_form.html')
    else:
        return redirect(url_for('/.sign_in'))


@asset_blueprint.route('/printable/<int:asset_id>', methods=['GET'])
def printable_view(asset_id: int):
    if g.user:
        asset: Asset = asset_service.get_specific_user_asset(g.user, asset_id)
        return render_template('printable_view_of_asset.html', asset_unique_identifier=asset.uniqueIdentifier)
    else:
        return redirect(url_for('/.sign_in'))

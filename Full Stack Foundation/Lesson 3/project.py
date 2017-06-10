from flask import Flask, jsonify, flash, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Making an API Endpoint (Get Request)
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html',restaurant=restaurant, items=items)

@app.route('/newmenuitem/<int:restaurant_id>/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New Menu Item created")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/editmenuitem/<int:restaurant_id>/<int:menu_id>/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id,):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		item.name = request.form['name']
		session.add(item) 
		session.commit()
		flash("Menu Item Edited successfully")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant_id=restaurant_id,item=item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/deletemenuitem/<int:restaurant_id>/<int:menu_id>/',methods=['POST','GET'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
    	session.delete(item)
    	session.commit()
    	flash("Menu Item Deleted successfully")
    	return url_for('restaurantMenu',restaurant_id)
    else:
    	return render_template('deletemenuitem.html',restaurant_id=restaurant_id,item=item)

if __name__=='__main__':
	app.secret_key='shubh23'
	app.debug = True
	app.run(host='0.0.0.0',port=5000)
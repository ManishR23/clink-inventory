import os
from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('clink.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        color TEXT,
        color_id TEXT,
        price_clink REAL,
        price_home_depot REAL,
        available INTEGER,
        length_in REAL,
        width_in REAL,
        height_in REAL,
        num_holes INTEGER
	)''')

    conn.commit()
    conn.close()

    # Main Page
    @app.route('/')
    def index():
        conn = sqlite3.connect('clink.db')
        c = conn.cursor()
        c.execute("SELECT * FROM inventory")
        items = c.fetchall()
        conn.close()

        return render_template('index.html', items=items)
    

    # Add Page
@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		data = (
			request.form['name'],
			request.form['category'],
			request.form['color'],
			request.form['color_id'],
			float(request.form['price_clink']),
			float(request.form['price_home_depot']),
			int(request.form['available']),
			float(request.form['length_in']),
			float(request.form['width_in']),
			float(request.form['height_in']),
			int(request.form['num_holes'])
		)
				
		conn = sqlite3.connect('clink.db')
		c = conn.cursor()
		c.execute('''INSERT INTO inventory
			(name, category, color, color_id, price_clink, price_home_depot, available, 
			length_in, width_in, height_in, num_holes)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
				    
					
		conn.commit()
		conn.close()
		return redirect('/')
			
	return render_template('add.html')

# Remove Page
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
      conn = sqlite3.connect('clink.db')
      c = conn.cursor()
      c.execute("DELETE FROM inventory WHERE id= ?", (item_id,))
      conn.commit()
      conn.close()
      return redirect('/')

#Edit Page
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    conn = sqlite3.connect('clink.db')
    c = conn.cursor()

    if request.method == 'POST':
        updated_data = (
            request.form['name'],
            request.form['category'],
            request.form['color'],
            request.form['color_id'],
            float(request.form['price_clink']),
            float(request.form['price_home_depot']),
            int(request.form['available']),
            float(request.form['length_in']),
            float(request.form['width_in']),
            float(request.form['height_in']),
            int(request.form['num_holes']),
            item_id
        )
        c.execute('''UPDATE inventory SET
                        name = ?, category = ?, color = ?, color_id = ?,
                        price_clink = ?, price_home_depot = ?, available = ?,
                        length_in = ?, width_in = ?, height_in = ?, num_holes = ?
                     WHERE id = ?''', updated_data)
        conn.commit()
        conn.close()
        return redirect('/')
    
    # GET request – load the existing item to populate the form
    c.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
    item = c.fetchone()
    conn.close()
    return render_template('edit.html', item=item)



if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Use Render’s port, default to 5000 for local dev
    app.run(host='0.0.0.0', port=port)

    

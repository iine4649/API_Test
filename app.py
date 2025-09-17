from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests


"""
Use a different API from https://github.com/public-apis/public-apis
Add multiple routes and use query parameters in your application
Utilize a form which will direct user to new route with information that was submitted by user.
Push to github and submit URL to repo into Canvas assignment
"""
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/get-quote")
def get_quote():
    try:
        response = requests.get("https://api.breakingbadquotes.xyz/v1/quotes")
        response.raise_for_status()  
        data = response.json()
        
        # ターミナルにクォートを表示
        quote = data[0]['quote']
        author = data[0]['author']
        print("\n" + "="*50)
        print("📝 Breaking Bad Quote:")
        print(f"💬 \"{quote}\"")
        print(f"👤 - {author}")
        print("="*50 + "\n")
        
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500
    except ValueError as e:
        error_msg = f"Invalid JSON response: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

@app.route("/search-quotes")
def search_quotes():
    """クエリパラメータでクォートを検索"""
    author = request.args.get('author', '')
    limit = request.args.get('limit', '1')
    
    try:
        # 複数のクォートを取得
        response = requests.get(f"https://api.breakingbadquotes.xyz/v1/quotes/{limit}")
        response.raise_for_status()
        data = response.json()
        
        # 作者でフィルタリング
        if author:
            filtered_data = [quote for quote in data if author.lower() in quote['author'].lower()]
            data = filtered_data
        
        # ターミナルに表示
        print(f"\n🔍 Search Results (Author: {author or 'All'}, Limit: {limit}):")
        for i, quote_data in enumerate(data, 1):
            print(f"{i}. \"{quote_data['quote']}\" - {quote_data['author']}")
        print("="*50 + "\n")
        
        return jsonify({
            "search_params": {"author": author, "limit": limit},
            "results": data,
            "count": len(data)
        })
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

@app.route("/random-fact")
def random_fact():
    """ランダムな事実を取得"""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        response.raise_for_status()
        data = response.json()
        
        fact = data['text']
        print(f"\n📚 Random Fact: {fact}")
        print("="*50 + "\n")
        
        return jsonify({
            "fact": fact,
            "source": "Useless Facts API"
        })
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg}), 500

@app.route("/submit-form", methods=['GET', 'POST'])
def submit_form():
    """フォーム処理"""
    if request.method == 'POST':
        name = request.form.get('name', '')
        favorite_character = request.form.get('character', '')
        message = request.form.get('message', '')
        
        # ターミナルに表示
        print(f"\n📝 Form Submission:")
        print(f"Name: {name}")
        print(f"Favorite Character: {favorite_character}")
        print(f"Message: {message}")
        print("="*50 + "\n")
        
        return redirect(url_for('form_result', 
                              name=name, 
                              character=favorite_character, 
                              message=message))
    
    return render_template('form.html')

@app.route("/form-result")
def form_result():
    """フォーム結果表示"""
    name = request.args.get('name', '')
    character = request.args.get('character', '')
    message = request.args.get('message', '')
    
    return render_template('result.html', 
                         name=name, 
                         character=character, 
                         message=message)

@app.route("/api-info")
def api_info():
    """API情報を表示"""
    apis = [
        {
            "name": "Breaking Bad Quotes",
            "url": "https://api.breakingbadquotes.xyz/v1/quotes",
            "description": "Breaking Badの名言を取得"
        },
        {
            "name": "Useless Facts",
            "url": "https://uselessfacts.jsph.pl/random.json",
            "description": "ランダムな面白い事実を取得"
        }
    ]
    
    return jsonify({
        "available_apis": apis,
        "endpoints": [
            "/get-quote - Breaking Badの名言を取得",
            "/search-quotes?author=Walter&limit=3 - 特定の作者の名言を検索",
            "/random-fact - ランダムな事実を取得",
            "/submit-form - フォーム送信",
            "/api-info - このAPI情報"
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)
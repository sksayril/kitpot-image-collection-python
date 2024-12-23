from flask import Flask, request, jsonify
from webscout import WEBS
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/search_images', methods=['POST'])
def search_images():
    try:
        # Get the keyword from the request
        data = request.json
        keyword = data.get('keyword')
        
        if not keyword:
            return jsonify({"error": "Keyword is required."}), 400

        # Search for images using WEBS
        image_urls = []
        with WEBS() as WEBS_instance:
            WEBS_images_gen = WEBS_instance.images(
                keywords=keyword,
                region="wt-wt",
                safesearch="off",
                size=None,
                type_image=None,
                layout=None,
                license_image=None,
                max_results=15,
            )

            # Collect image URLs
            for result in WEBS_images_gen:
                if 'image' in result:
                    image_urls.append(result['image'])

        # Return the image URLs as a response
        return jsonify({"keyword": keyword, "image_urls": image_urls})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

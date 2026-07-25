import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image_path):
	results = reader.readtext(image_path, detail=0)
	return " ".join(results)

if __name__ == '__main__':
	# simple CLI for quick testing
	import sys
	if len(sys.argv) > 1:
		print(extract_text(sys.argv[1]))
	else:
		print('Usage: python ocr.py <image_path>')

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;  //for making http requests
import 'dart:convert';   //json encoding and decoding krne ke use ata hai

Future<void> main() async {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CloudPix',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ImageGalleryScreen(),
    );
  }
}

class ImageGalleryScreen extends StatefulWidget {
  @override
  _ImageGalleryScreenState createState() => _ImageGalleryScreenState();
}

class _ImageGalleryScreenState extends State<ImageGalleryScreen> {
  List<String> imageUrls = [];

  @override
  void initState() {
    super.initState();
    fetchImages();
  }


  Future<void> fetchImages() async {   //flask api se image fetch karke layega
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/images'));
    if (response.statusCode == 200) {
      setState(() {
        imageUrls = List<String>.from(json.decode(response.body));
      });
    } else {
      print('Failed to load images');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('CloudPix')),
      body: imageUrls.isEmpty
          ? Center(child: CircularProgressIndicator())
          : GridView.builder(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 1,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
              ),
              itemCount: imageUrls.length,
              itemBuilder: (context, index) {
                return Image.network(imageUrls[index]);
              },
            ),
    );
  }
}

//
//  Awesomation.swift
//  Awesomation
//
//  Created by Tom Wilkie on 29/01/2015.
//  Copyright (c) 2015 Awesomation. All rights reserved.
//

import Foundation

class Awesomation {

    struct Constants {
        static let SCHEME = "https"
        static let HOST = "homeawesomation.appspot.com"
        static let POST = "POST"
    }
    
    class func post(path: String, data: [String: String]) -> Awesomation {
        var url = NSURL(scheme: Constants.SCHEME, host: Constants.HOST, path: path)
        var data = NSJSONSerialization.dataWithJSONObject(data, options:nil, error:nil)
        var request = NSMutableURLRequest(URL: url!)
        request.HTTPMethod = Constants.POST
        request.HTTPBody = data
        
        var awesomation = Awesomation()
        var connection = NSURLConnection(request: request, delegate: awesomation)
        return awesomation
    }
    
    var data: NSMutableData;
    
    init() {
        data = NSMutableData()
    }
    
    func connection(didReceiveResponse: NSURLConnection!, didReceiveResponse response: NSURLResponse!) {
        println("didReceiveResponse")
    }
    
    func connection(connection: NSURLConnection!, didReceiveData conData: NSData!) {
        self.data.appendData(conData)
    }
    
    func connectionDidFinishLoading(connection: NSURLConnection!) {
        println(self.data)
    }

}
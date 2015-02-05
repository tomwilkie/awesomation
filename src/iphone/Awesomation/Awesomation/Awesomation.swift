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
        static let POST = "POST"
        static let GET = "GET"
        static let baseURL = NSURL(string: "https://homeawesomation.appspot.com")
    }
    
    var auth: GTMOAuth2Authentication
    var config: NSURLSessionConfiguration?
    var manager: AFHTTPRequestOperationManager
    
    init(auth:GTMOAuth2Authentication) {
        self.auth = auth
        self.manager = AFHTTPRequestOperationManager(baseURL: Constants.baseURL)
    }
    
    // T here for any type as I don't care what it returns - better way of doing this? 'a?
    func withToken<T>(block: (Void -> T)) {
        var fakerequest = NSMutableURLRequest()
        self.auth.authorizeRequest(fakerequest, { (error) in
            self.manager.requestSerializer.setValue("Bearer \(self.auth.accessToken)", forHTTPHeaderField:"Authorization")

            block()
        })
    }
    
    func get(path: String) {
        withToken({
            self.manager.GET(path, parameters: nil, success: { (op, result) in
                println(result)
            }, failure: { (op, error) in
                println(error)
            })
        })
    }
    
    /*func post(path: String, data: [String: String]) {
        var url = NSURL(scheme: Constants.SCHEME, host: Constants.HOST, path: path)
        var data = NSJSONSerialization.dataWithJSONObject(data, options:nil, error:nil)
        var request = NSMutableURLRequest(URL: url!)
        request.HTTPMethod = Constants.POST
        request.HTTPBody = data
        
        self.auth.authorizeRequest(request)
        
        var connection = NSURLConnection(request: request, delegate: self)
    }*/
}
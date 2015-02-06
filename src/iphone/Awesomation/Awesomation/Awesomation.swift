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
        static let BASE_URL = NSURL(string: "https://homeawesomation.appspot.com")
    }

    var auth: GTMOAuth2Authentication
    var config: NSURLSessionConfiguration?
    var manager: AFHTTPRequestOperationManager

    init(auth:GTMOAuth2Authentication) {
        self.auth = auth
        self.manager = AFHTTPRequestOperationManager(baseURL: Constants.BASE_URL)
        self.manager.requestSerializer = AFJSONRequestSerializer(writingOptions: NSJSONWritingOptions())
        self.manager.responseSerializer = AFJSONResponseSerializer()
    }

    func withToken(block: (Void -> Any)) {
        var fakerequest = NSMutableURLRequest()
        self.auth.authorizeRequest(fakerequest, { (error) in
            self.manager.requestSerializer.setValue("Bearer \(self.auth.accessToken)", forHTTPHeaderField:"Authorization")

            block()
        })
    }

    func get(path: String, success: ([String: AnyObject] -> Void)) {
        withToken({
            self.manager.GET(path, parameters: nil, success: { (op, result) in
                success(result as [String: AnyObject])
            }, failure: { (op, error) in
                println(error)
            })
        })
    }

    func post(path: String, data: [String: String], success: ([String: AnyObject] -> Void)) {
        var data = NSJSONSerialization.dataWithJSONObject(data, options:nil, error:nil)
        
        withToken({
            self.manager.GET(path, parameters: data, success: { (op, result) in
                success(result as [String: AnyObject])
            }, failure: { (op, error) in
                    println(error)
            })
        })
    }
}


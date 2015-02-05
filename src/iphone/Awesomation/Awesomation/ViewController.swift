//
//  ViewController.swift
//  Awesomation
//
//  Created by Tom Wilkie on 29/01/2015.
//  Copyright (c) 2015 Awesomation. All rights reserved.
//

import UIKit
import CoreLocation

class ViewController: UIViewController, CLLocationManagerDelegate  {
    
    struct Constants {
        static let KEYCHAIN_ITEM_NAME = "Awesomeation Credentials"
        static let SCOPE = "https://www.googleapis.com/auth/userinfo.email"
    }
    
    let RADIUS: CLLocationDistance = 10;
    var locationManager: CLLocationManager!
    var currentLocation: CLLocation!
    var auth: GTMOAuth2Authentication?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestAlwaysAuthorization()
        
        locationManager.startUpdatingLocation()
    }
    
    override func viewDidAppear(animated: Bool) {
        self.doAuth();
    }

    func doAuth() {
        
        self.auth = GTMOAuth2ViewControllerTouch.authForGoogleFromKeychainForName(
            Constants.KEYCHAIN_ITEM_NAME,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET)

        if self.auth != nil && self.auth!.canAuthorize {
            println("Loaded auth cookie from keychain")
            doRequest()
            return
        }
        
        var gtmOauthView = GTMOAuth2ViewControllerTouch(
            scope:Constants.SCOPE,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET,
            keychainItemName:Constants.KEYCHAIN_ITEM_NAME,
            completionHandler: {(viewController, auth, error) in
                println(auth)
                
                // Get rid of the login view.
                // self.parentViewController was saved somewhere else and is the parent
                // view controller of the view controller that shows the google login view.
                self.navigationController?.dismissViewControllerAnimated(true, completion: nil)
                viewController.removeFromParentViewController()
                
                if error != nil {
                    // Authentication failed
                } else {
                    self.auth = auth
                    self.doRequest()
                }
        })
        
        self.navigationController!.presentViewController(gtmOauthView, animated: true, completion: nil)
    }
    
    @IBAction func doLogout(sender: AnyObject) {
        GTMOAuth2ViewControllerTouch.removeAuthFromKeychainForName(Constants.KEYCHAIN_ITEM_NAME)
    }
    

    @IBAction func requestClick(sender: AnyObject) {
        doRequest()
    }
    
    func doRequest() {
        println("Doing request")
        var awesomation = Awesomation(auth:self.auth!)
        awesomation.get("/api/device/")
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func locationManager(manager: CLLocationManager!, didUpdateLocations locations: [AnyObject]!) {
        if currentLocation == nil {
            currentLocation = locations[locations.count - 1] as CLLocation
            println("\(currentLocation)")
            locationManager.stopUpdatingLocation()
        }
    }
    
    @IBAction func registerLocation(sender: UIButton) {
        var radius = RADIUS
        var homeLocation = currentLocation

        if currentLocation == nil {
            println("Current location is nil")
            return
        }
    
        if radius > locationManager.maximumRegionMonitoringDistance {
            radius = locationManager.maximumRegionMonitoringDistance;
        }
        
        // Create the geographic region to be monitored.
        var region = CLCircularRegion(
            circularRegionWithCenter: currentLocation.coordinate,
            radius: radius, identifier: "Home")

        println("startMonitoringForRegion \(region)")
        locationManager.startMonitoringForRegion(region)
        
        locationManager.requestStateForRegion(region)
    }
    
    func locationManager(manager: CLLocationManager!, didDetermineState state: CLRegionState, forRegion region: CLRegion!) {
        println("\(region) is \(state)")
    }

}


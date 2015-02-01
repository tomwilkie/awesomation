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

    let RADIUS: CLLocationDistance = 10;
    var locationManager: CLLocationManager!
    var currentLocation: CLLocation!
    var auth: GTMOAuth2Authentication?;
    
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
        var kKeychainItemName = "Awesomeation OAuth"
        var scope = "https://www.googleapis.com/auth/userinfo.email"
        
        self.auth = GTMOAuth2ViewControllerTouch.authForGoogleFromKeychainForName(
            kKeychainItemName,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET)

        if self.auth != nil && self.auth!.canAuthorize {
            println("Loaded auth cookie from keychain")
            return
        }
        
        var viewController: GTMOAuth2ViewControllerTouch = GTMOAuth2ViewControllerTouch(
            scope:scope,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET,
            keychainItemName:kKeychainItemName,
            delegate:self,
            finishedSelector:"viewController:finishedWithAuth:error:")
        
        self.presentViewController(viewController, animated: true, completion: nil)
    }
    
    func viewController(viewController: GTMOAuth2ViewControllerTouch,
        finishedWithAuth: GTMOAuth2Authentication, error: NSError?) {
        println("\(error)")
        if error != nil {
            // Authentication failed
        } else {
            self.auth = finishedWithAuth;
        }
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


//
//  ViewController.swift
//  Awesomation
//
//  Created by Tom Wilkie on 29/01/2015.
//  Copyright (c) 2015 Awesomation. All rights reserved.
//

import AddressBookUI
import CoreLocation
import UIKit


class ViewController: UIViewController, CLLocationManagerDelegate  {
    
    struct Constants {
        static let KEYCHAIN_ITEM_NAME = "Awesomeation Credentials"
        static let SCOPE = "https://www.googleapis.com/auth/userinfo.email"
        static let RADIUS: CLLocationDistance = 10
        static let HOME = "Home"
        static let YOU_ARE_HOME = "You are home."
        static let YOU_ARE_NOT_HOME = "You are not home."
        static let ESTIMOTE_UUID = "B9407F30-F5F8-466E-AFF9-25556B57FE6D"
        static let ESTIMOTE_BEACONS = "Estimote Beacons"
    }
    
    var locationManager: CLLocationManager!
    var currentLocation: CLLocation!
    var geocoder: CLGeocoder?
    var auth: GTMOAuth2Authentication?
    
    var home: CLCircularRegion?
    var homeAddress: String?
    var amInHome = false
    
    @IBOutlet weak var homeTextView: UITextView!
    @IBOutlet weak var homeStateView: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestAlwaysAuthorization()
        locationManager.startUpdatingLocation()
        
        var estimoteBeacons = CLBeaconRegion(proximityUUID: NSUUID(UUIDString: Constants.ESTIMOTE_UUID),
            identifier: Constants.ESTIMOTE_BEACONS)
        estimoteBeacons.notifyEntryStateOnDisplay = true
        locationManager.startMonitoringForRegion(estimoteBeacons)
        locationManager.startRangingBeaconsInRegion(estimoteBeacons)
        
        geocoder = CLGeocoder()
        
        updateHome()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewDidAppear(animated: Bool) {
        self.doAuth();
    }
    
    func updateUI() {
        dispatch_async(dispatch_get_main_queue(), {
            self.homeTextView.text = self.homeAddress
            self.homeStateView.text = self.amInHome ? Constants.YOU_ARE_HOME : Constants.YOU_ARE_NOT_HOME
        })
    }
    
    func findRegionByName(name: String) -> CLRegion? {
        for region in locationManager.monitoredRegions {
            var region = region as CLRegion
            if region.identifier == name {
                return region
            }
        }
        return nil
    }
    
    func updateHome() {
        self.home = findRegionByName(Constants.HOME) as? CLCircularRegion;
        if home == nil {
            self.homeAddress = "None"
            self.updateUI()
            return
        }
        
        var location = CLLocation(latitude:home!.center.latitude, longitude:home!.center.longitude)
        geocoder?.reverseGeocodeLocation(location, completionHandler: { (placemarks, error) -> Void in
            if placemarks == nil || placemarks!.count == 0 {
                self.homeAddress = "\(location)"
            } else {
                var placemark = placemarks[0] as CLPlacemark
                self.homeAddress = ABCreateStringWithAddressDictionary(placemark.addressDictionary, false)
            }
            self.updateUI()
        })
    }
  
    @IBAction func setCurrentLocationAsHome(sender: AnyObject) {
        var radius = Constants.RADIUS
        var homeLocation = currentLocation
        
        if currentLocation == nil {
            NSLog("Current location is nil")
            return
        }
        
        if radius > locationManager.maximumRegionMonitoringDistance {
            radius = locationManager.maximumRegionMonitoringDistance;
        }
        
        // Create the geographic region to be monitored.
        var region = CLCircularRegion(
            circularRegionWithCenter: currentLocation.coordinate,
            radius: radius, identifier: Constants.HOME)
        
        NSLog("startMonitoringForRegion \(region)")
        locationManager.startMonitoringForRegion(region)
        locationManager.requestStateForRegion(region)
        
        self.updateHome()
    }
    
    func locationManager(manager: CLLocationManager!, didUpdateLocations locations: [AnyObject]!) {
        NSLog("didUpdateLocations \(locations)")
        
        if currentLocation == nil {
            currentLocation = locations[locations.count - 1] as CLLocation
            locationManager.stopUpdatingLocation()
        }
    }
    
    func locationManager(manager: CLLocationManager!, didDetermineState state: CLRegionState, forRegion region: CLRegion!) {
        if region.identifier == Constants.HOME {
            amInHome = state == CLRegionState.Inside
            updateUI()
        }
    }
    
    func doAuth() {
        self.auth = GTMOAuth2ViewControllerTouch.authForGoogleFromKeychainForName(
            Constants.KEYCHAIN_ITEM_NAME,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET)

        if self.auth != nil && self.auth!.canAuthorize {
            NSLog("Loaded auth cookie from keychain")
            getDevices()
            return
        }
        
        var gtmOauthView = GTMOAuth2ViewControllerTouch(
            scope:Constants.SCOPE,
            clientID:Credentials.GOOGLE_CLIENT_ID,
            clientSecret:Credentials.GOOGLE_CLIENT_SECRET,
            keychainItemName:Constants.KEYCHAIN_ITEM_NAME,
            completionHandler: {(viewController, auth, error) in
                NSLog("\(auth)")
                
                // Get rid of the login view.
                // self.parentViewController was saved somewhere else and is the parent
                // view controller of the view controller that shows the google login view.
                //self.navigationController?.dismissViewControllerAnimated(true, completion: nil)
                //viewController.removeFromParentViewController()
                
                if error != nil {
                    // Authentication failed
                } else {
                    self.auth = auth
                    self.getDevices()
                }
        })
        
        self.navigationController!.pushViewController(gtmOauthView, animated: true)
    }
    
    @IBAction func doLogout(sender: AnyObject) {
        NSLog("doLogout")
        GTMOAuth2ViewControllerTouch.removeAuthFromKeychainForName(Constants.KEYCHAIN_ITEM_NAME)
        doAuth()
    }
    
    func getDevices() {
        NSLog("getDevices")
        var awesomation = Awesomation(auth:self.auth!)
    }
}


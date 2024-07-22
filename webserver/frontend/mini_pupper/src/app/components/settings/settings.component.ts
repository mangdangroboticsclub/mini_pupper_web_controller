import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

type Ret = {
    [key: string]: any;
};

@Injectable({
    providedIn: 'root'
})
@Component({
    selector: 'app-settings',
    templateUrl: './settings.component.html',
    styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

    ssid: string = '';
    password: string = '';


    private REST_API_SERVER = window.location.protocol + '//' + window.location.host + this.router.url

    loading: boolean=false;

    constructor(private http: HttpClient, private router: Router) { }

    getHttp(ssid: string, password: string): void {
        this.loading = true;
        this.http.get<Ret>(this.REST_API_SERVER + '/'  + ssid + '/' + password)
        .subscribe(data => {
            this.loading = false;
            console.log(data);
        },
        error => {
            console.log(error);
            this.loading = false;
        }
                  );

    }

    ngOnInit(): void {
    }

    onChange(slider: string, value: number | null): void{
        if(value) {
            this.getHttp(slider, value.toString())
        }
    }

    onClick(ssid: string, password: string): void {
        this.getHttp(ssid, password)
    }

    onShellClick(command: string): void {
        this.getHttp("shell_cmd", command)
    }
}

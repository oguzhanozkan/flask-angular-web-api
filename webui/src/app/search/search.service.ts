import { Injectable } from '@angular/core'
import { HttpClient} from '@angular/common/http'
import { Observable } from 'rxjs'
import {environment} from '../../environments/environment'
import { Rss } from '../rss/rss'


@Injectable()
export class SearchService {
    constructor(private http:HttpClient) { }

    rss:Rss[]
    private GET_RSS_WITH_DATE = "/get_rss_with_date"

    dates =  {
        start_date:Date,
        end_date: Date
    }

    
    getRssWithDate(dates):Observable<Rss[]>{
       return this.http.post<Rss[]>(environment.API_BASE_PATH + this.GET_RSS_WITH_DATE, dates)
    }
}

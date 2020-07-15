import { Component, OnInit } from '@angular/core'
import { Rss } from './rss'
import { RssService } from './rss.service'


@Component({
    selector: 'app-rss',
    templateUrl: './rss.component.html',
})

export class RssComponent implements OnInit {

    rss: Rss[]
    rss_field: Rss
    pageCurrent: number = 1
    constructor(private rssService: RssService) { }

    ngOnInit() {
        this.rssService.getRssAll().subscribe(
            rss => {
                this.rss = rss
            }
        )
    }
}

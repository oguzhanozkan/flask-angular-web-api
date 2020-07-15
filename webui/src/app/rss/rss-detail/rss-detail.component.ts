import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RssService } from '../rss.service';
import { Rss } from '../rss';

declare let alertify: any

@Component({
  selector: 'app-rss-detail',
  templateUrl: './rss-detail.component.html',
  styleUrls: ['./rss-detail.component.css']
})
export class RssDetailComponent implements OnInit {

  id: string
  private detail: any
  rss_description: string
  rss_link: string
  rss_data: Rss
  constructor(private route: ActivatedRoute, private rssService: RssService) { }

  ngOnInit() {
    this.detail = this.route.params.subscribe(params => {
      this.id = params['id']
    });
    console.log(this.id)
    this.rssService.getRssById(this.id).subscribe(
      res => {
        if (res) {
          this.rss_data = res
          this.rss_description = res.description
          this.rss_link = res.link
        } else {
          alertify.warning('error')
        }
      }
    )
  }

  AddFav(id) {
    this.rssService.addFavori(id, this.rss_data).subscribe(
      data => {
        if (data) {
          console.log(this.rss_data)
          alertify.success('eklendi')
        } else {
          return {}
        }
      }
    )
  }
}

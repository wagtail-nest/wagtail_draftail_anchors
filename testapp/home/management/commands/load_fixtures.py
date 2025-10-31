from django.core.management.base import BaseCommand
from wagtail.models import Page


class Command(BaseCommand):
    help = "Load initial fixtures for the testapp"

    def handle(self, *args, **options):
        # get the home page
        home_page_id = Page.objects.get(slug="home").id
        home_page = Page.objects.get(id=home_page_id).specific

        # load fixtures
        home_page.body = (
            '<p data-block-key="vh8tr"><a href="#section-heading">To Section Heading</a></p>'
            '<p data-block-key="dp245"><a href="#sub-heading">To Sub Heading</a></p>'
            '<p data-block-key="f9pk9"><a href="#another-section">To Another Section</a></p>'
            '<p data-block-key="2j7eq"><a href="#footer">To Footer</a></p>'
            '<p data-block-key="3p0nv">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<p data-block-key="e2os0">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<p data-block-key="2fsdb">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<p data-block-key="esklk">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<h2 id="section-heading" data-block-key="f93sx">'
            '<a data-id="section-heading" id="section-heading" href="#section-heading" linktype="anchor-target">'
            '<b>Section Heading</b></a></h2>'
            '<p data-block-key="d53nh">Curabitur pretium, tellus id vulputate convallis, nibh magna pretium mi, in porta dui lacus vitae odio. Morbi posuere sem sit amet urna imperdiet, id gravida elit elementum. Suspendisse potenti. Phasellus non consequat justo. Donec eget tortor ac nibh interdum suscipit.</p>'
            '<p data-block-key="841le">Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In hac habitasse platea dictumst. Vivamus fringilla, mi non faucibus aliquam, orci nulla interdum mauris, nec euismod arcu nisi at nisl.</p>'
            '<p data-block-key="2b9j3">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<p data-block-key="u322">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<p data-block-key="f65ng">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <b>Amet</b> vitae volutpat nunc, at facilisis erat. Integer nec augue quis arcu posuere pellentesque. Sed ultricies, turpis quis faucibus fermentum, risus tortor congue orci, non placerat velit arcu vel mi.</p>'
            '<h2 id="subheading" data-block-key="ngm35">'
            '<a data-id="sub-heading" id="sub-heading" href="#sub-heading" linktype="anchor-target">'
            '<b>Subheading</b></a></h2>'
            '<p data-block-key="5rqjf">Aliquam eu dui non turpis auctor tristique. Duis cursus velit at sapien interdum, vitae sodales libero commodo. Proin quis nibh sem. Nullam luctus, metus a pulvinar tempor, lorem justo ullamcorper urna, vitae <b>31 October</b> varius ante mi at nisl.</p>'
            '<p data-block-key="8mohr"><b>Intro:</b> Praesent vitae diam nec nisl interdum facilisis.</p>'
            '<p data-block-key="a144f"><b>Body:</b> Cras laoreet sapien at augue lobortis, sit amet tristique magna.</p>'
            '<p data-block-key="2jpnc"><b>Detail:</b> Maecenas at erat a tellus varius tristique.</p>'
            '<p data-block-key="4mrhh"><b>Note:</b> Aenean sodales dui nec magna bibendum.</p>'
            '<p data-block-key="6arc4"><b>Summary:</b> Sed porttitor arcu sed felis tempus luctus.</p>'
            '<h2 id="another-section" data-block-key="0znbi">'
            '<a data-id="another-section" id="another-section" href="#another-section" linktype="anchor-target">'
            '<b>Another Section</b></a></h2>'
            '<p data-block-key="2qmhk">Nam at lectus arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Integer dignissim, justo sed convallis posuere, orci dolor ultricies augue, id iaculis mi nibh sed neque. Quisque at pulvinar arcu. Suspendisse tristique est eu odio ullamcorper bibendum.</p>'
            '<p data-block-key="cntb3">Small Subsection</p>'
            '<p data-block-key="7q8c5">Fusce venenatis, nisl ut bibendum aliquet, mauris sapien porta purus, non viverra mauris odio non est. Aenean eget metus ac velit lacinia rutrum. Ut et tellus nec nisl imperdiet rhoncus. Cras dictum, urna quis convallis gravida, elit augue ultricies turpis, a tincidunt leo purus at quam.</p>'
            '<h2 id="footer" data-block-key="0vcwr">'
            '<a data-id="footer" id="footer" href="#footer" linktype="anchor-target">'
            '<b>Footer</b></a></h2>'
            '<p data-block-key="eabr2">Sed eu risus eu nibh congue pharetra. Curabitur sed sem id sapien auctor maximus. Integer accumsan, magna a mattis sollicitudin, est metus dapibus mi, vitae aliquet urna nisl non neque. Donec a dui non est efficitur ultrices.</p>'
        )
        revision = home_page.save_revision()
        revision.publish()

        self.stdout.write(self.style.SUCCESS("Successfully loaded initial fixtures for testapp"))
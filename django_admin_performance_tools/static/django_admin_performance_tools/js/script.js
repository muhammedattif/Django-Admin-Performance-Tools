
if (typeof django != "undefined")
    (function ($) {
        ListFilterCollapsePrototype = {
            bindToggle: function () {
                var that = this;
                this.$filterEl.click(function () {
                    that.$filterList.slideToggle();
                    that.$filterEl.find("span").toggleClass("open")
                });
            },
            init: function (filterEl, renderArrowSpan=true) {
                this.$filterEl = $(filterEl).css('cursor', 'pointer');
                if (renderArrowSpan){
                    this.$filterEl = $(filterEl).prepend("<span class='chevron'></span> ")
                }
                this.$filterList = this.$filterEl.next('ul').hide();
                if (this.$filterList.length <= 0) {
                    this.$filterList = this.$filterEl.nextAll('.admindatefilter:first').hide()
                    if (this.$filterList.find("input[type=text][value]").length > 0) {
                        this.$filterList = this.$filterList.show();
                        this.$filterEl.find("span").toggleClass("open");
                    }
                }
                else if (!this.$filterList.find("li:first").hasClass("selected")) {
                    this.$filterList = this.$filterList.show();
                    this.$filterEl.find("span").toggleClass("open");
                }
                this.bindToggle();
            }
        }
        function ListFilterCollapse(filterEl, renderArrowSpan) {
            this.init(filterEl, renderArrowSpan);
        }
        ListFilterCollapse.prototype = ListFilterCollapsePrototype;

        $(document).ready(function () {
            $('#changelist-filter').children('h3:not(#changelist-filter-clear)').each(function () {
                new ListFilterCollapse(this, true);
            });
            $('#changelist-filter').children('details:not(#changelist-filter-clear)').each(function () {
                const element = $(this);
                filterTxt = element.find("li[class=selected]").children('a')[0].href
                filterKey = element.attr("data-filter-title").replaceAll(" ", "_").toLowerCase();
                if (filterTxt.includes(filterKey)){
                    element.attr("open", "");
                }else{
                    element.removeAttr("open");
                }
            });
        });
    })(django.jQuery);

(function($){
    $.fn.multiInput = function(config){
        var extern = {};
        var prototypes = $(this).children();
        var addButton = $('<button type="button">').addClass('jquery-multiInput-add');
        addButton.html(config.addLabel != null ? config.addLabel : "Add");
        var removeButtonPrototype = $('<button type="button">').addClass('jquery-multiInput-delete');
        removeButtonPrototype.html(config.removeLabel != null ? config.removeLabel : "Remove");
        var container = $(this);
        var minFields = config.minFields != null ? config.minFields : 1;
        var maxFields = config.maxFields != null ? config.minFields : 10;
        var elemCount = 0;
        var replaceAttributes = function(element, index){
            var $elem = $(element);
            $.each(element.attributes, function(attribute, element){
                $elem.attr(this.name, $elem.attr(this.name).replace('#index#', index));
            });
            $(element).find('*').each(function(){
                var elem = this;
                var $elem = $(elem);
                $.each(elem.attributes, function(attribute){
                    var value = $elem.attr(this.name);
                    if (value.match('#index#')){
                        $elem.attr(this.name, value.replace('#index#', index));
                    }
                });
            });
        }
        var makeElement = function(){
            var newelems = prototypes.map(function(){
                var elem = $(this).clone();
                replaceAttributes(elem[0], elemCount);
                container.append(elem);
                return elem;
            });
            if (elemCount >= minFields) {
                var rmButton = removeButtonPrototype.clone();
                $(rmButton).click(function(){
                    $.each(newelems, function(){
                        $(this).remove();
                    });
                    elemCount -= 1;
                    $(this).remove();
                });
                container.append(rmButton);
            }
            elemCount += 1;
        }
        prototypes.remove();
        for (i = 0; i < minFields; i++){
            makeElement();   
        }
        addButton.click(function(){
            makeElement();
        });
        container.after(addButton);
   };
})(jQuery);

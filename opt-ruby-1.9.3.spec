%define rubyver         1.9.3
%define rubyminorver    p194

%define _prefix		/opt/ruby-%{rubyver}
%define _localstatedir	/opt/ruby-%{rubyver}/var
%define _mandir		/opt/ruby-%{rubyver}/man
%define _infodir	/opt/ruby-%{rubyver}/share/info

Name:           opt-ruby-%{rubyver}
Version:        %{rubyver}%{rubyminorver}
Release:        1%{?dist}
License:        Ruby License/GPL - see COPYING
URL:            http://www.ruby-lang.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  readline libyaml libyaml-devel readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel db4-devel byacc make
Requires:       libyaml
Source0:        ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.gz
Summary:        An interpreter of object-oriented scripting language
Group:          Development/Languages
Provides: opt-ruby-%{rubyver}(abi) = %{rubyver}
Provides: opt-ruby-%{rubyver}-irb
Provides: opt-ruby-%{rubyver}-rdoc
Provides: opt-ruby-%{rubyver}-libs
Provides: opt-ruby-%{rubyver}-devel
Provides: opt-ruby-%{rubyver}-rubygems

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -n ruby-%{rubyver}-%{rubyminorver}

%build

export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

%configure \
  --enable-shared \
  --disable-rpath \
  --libdir=/opt/ruby-%{rubyver}/lib

make RUBY_INSTALL_NAME=ruby %{?_smp_mflags}

%install
# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/opt/ruby-%{rubyver}/bin/ruby $RPM_BUILD_ROOT/opt/ruby-%{rubyver}/bin/ruby-bin
echo "#!/bin/sh
export LD_LIBRARY_PATH=/opt/ruby-%{rubyver}/lib
/opt/ruby-%{rubyver}/bin/ruby-bin \"\$@\"
" > $RPM_BUILD_ROOT/opt/ruby-%{rubyver}/bin/ruby
chmod +x $RPM_BUILD_ROOT/opt/ruby-%{rubyver}/bin/ruby

#we don't want to keep the src directory
#rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README COPYING ChangeLog LEGAL ToDo
%{_prefix}

%changelog
* Wed Apr 25 2012 mathew <meta@pobox.com> - 1.9.3-p194-1
- Update for Ruby 1.9.3-p194 release.
* Sat Feb 24 2012 Ian Meyer <ianmmeyer@gmail.com> - 1.9.3-p125-1
- Spec to replace system ruby with 1.9.3-p125


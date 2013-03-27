%define gemname flexmock
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']" 2>/dev/null)
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Name:		opt-ruby-%{rubyver}-rubygem-%{gemname}
Summary:	Mock object library for ruby (REE)
Version:	0.8.6
Release:	1%{?dist}
Group:		Development/Languages
License:	Copyright only
URL:		http://flexmock.rubyforge.org
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	opt-ruby-%{rubyver}
#BuildRequires(check):	ree-rubygem(rake) = 0.9.2.2
Requires:	opt-ruby-%{rubyver}
Provides:	opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{name}-%{version}
BuildArch:	noarch

%description
FlexMock is a simple, but flexible, mock object library for Ruby unit
testing.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%package	-n opt-ruby-%{rubyver}-%{gemname}
Summary:	Non-Gem support package for %{gemname}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	opt-ruby-%{rubyver}(%{gemname}) = %{version}-%{release}

%description    -n opt-ruby-%{rubyver}-%{gemname}
This package provides non-Gem support for %{gemname}.

%prep
%setup -q -c -T

mkdir -p .%{gemdir}
%{ruby_dir}/bin/gem install \
	--local \
	--install-dir .%{gemdir} \
	--force --rdoc -V \
	%{SOURCE0}

find . -name \*.rb | xargs sed -i -e '\@/usr/bin/env@d'
find . -name \*.gem -or -name \*.rb -or -name \*.rdoc | xargs chmod 0644

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

# Create symlinks
# Copied from rubygem-getetxt.spec
##
## Note that before switching to gem %%{ruby_sitelib}/%%{gemname}
## already existed as a directory, so this cannot be replaced
## by symlink (cpio fails)
## Similarly, all directories under %%{ruby_sitelib} cannot be
## replaced by symlink
#

create_symlink_rec(){

ORIGBASEDIR=$1
TARGETBASEDIR=$2

## First calculate relative path of ORIGBASEDIR 
## from TARGETBASEDIR
TMPDIR=$TARGETBASEDIR
BACKDIR=
DOWNDIR=
num=0
nnum=0
while true
do
	num=$((num+1))
	TMPDIR=$(echo $TMPDIR | %{__sed} -e 's|/[^/][^/]*$||')
	DOWNDIR=$(echo $ORIGBASEDIR | %{__sed} -e "s|^$TMPDIR||")
	if [ x$DOWNDIR != x$ORIGBASEDIR ]
	then
		nnum=0
		while [ $nnum -lt $num ]
		do
			BACKDIR="../$BACKDIR"
			nnum=$((nnum+1))
		done
		break
	fi
done

RELBASEDIR=$( echo $BACKDIR/$DOWNDIR | %{__sed} -e 's|//*|/|g' )

## Next actually create symlink
pushd %{buildroot}/$ORIGBASEDIR
find . -type f | while read f
do
	DIRNAME=$(dirname $f)
	BACK2DIR=$(echo $DIRNAME | %{__sed} -e 's|/[^/][^/]*|/..|g')
	%{__mkdir_p} %{buildroot}${TARGETBASEDIR}/$DIRNAME
	LNNAME=$(echo $BACK2DIR/$RELBASEDIR/$f | \
		%{__sed} -e 's|^\./||' | %{__sed} -e 's|//|/|g' | \
		%{__sed} -e 's|/\./|/|' )
	%{__ln_s} -f $LNNAME %{buildroot}${TARGETBASEDIR}/$f
done
popd

}

create_symlink_rec %{geminstdir}/lib %{ruby_sitelib}

%clean
rm -rf %{buildroot}

%check
pushd .%{geminstdir}
#%{ruby_dir}/bin/rake test_all --trace

%files
%defattr(-,root,root,-)
%dir	%{geminstdir}
%doc	%{geminstdir}/[A-Z]*
%exclude	%{geminstdir}/Rakefile
%exclude	%{geminstdir}/install.rb
%{geminstdir}/lib/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/flexmock.blurb
%{geminstdir}/doc/
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{version}/

%files	-n opt-ruby-%{rubyver}-%{gemname}
%defattr(-,root,root,-)
%{ruby_sitelib}/%{gemname}.rb
%{ruby_sitelib}/%{gemname}/

%changelog
* Thu Jul 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.6-1
- Switch to gem, repackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 08 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-3
- Fix repoid 

* Wed Nov 07 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-2
- Spec cleanups in response to review
- Fix license
- strip out shebangs

* Sun Sep 09 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-1
- Initial vesion
